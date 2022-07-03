from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from glossary.application.utils import auth_user, get_glossary_repo
from glossary.src.core.services.jwt_auth import auth_service

from glossary.src.core.entity.base import User
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.exception.base import AuthError, RepoError
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

class UserSchema(BaseModel):
    name: str = Field(max_length=30, min_length=5)
    password: str = Field(max_length=30, min_length=5)

class UserSchemaResponce(UserSchema):
    id: int

class LoginResponce(BaseModel):
    token: str

@router.post("/register", response_model=UserSchemaResponce)
def register(
    user_data: UserSchema = Body(),
    repo: IGlossarySQLRepo = Depends(get_glossary_repo)
):
    try:
        user = repo.save_user(
            CreateUserDTO(name=user_data.name, password=user_data.password)
        )
    except RepoError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return JSONResponse(content=jsonable_encoder(user))

@router.post("/login", response_model=LoginResponce)
def login(
    user_data: UserSchema = Body(),
    repo: IGlossarySQLRepo = Depends(get_glossary_repo)
):
    try:
        token = auth_service.login(
            name=user_data.name,
            password=user_data.password,
            repo=repo
        )
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))
    return JSONResponse(content=jsonable_encoder(LoginResponce(token=token)))

@router.get("/me", response_model=UserSchemaResponce)
def me(user: User = Depends(auth_user)):
    return JSONResponse(content=jsonable_encoder(user))

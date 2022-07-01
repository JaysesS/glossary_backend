from typing import Union
from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from glossary.application.database.holder import db
from glossary.src.core.services.jwt_auth import auth_service
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.exception.base import AuthError, RepoError
from glossary.src.data.repo.user.repo import UserRepo

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

class UserSchema(BaseModel):
    name: str = Field(description="Username", max_length=30, min_length=5)
    password: str = Field(description="Password", max_length=30, min_length=5)

class UserSchemaResponce(UserSchema):
    id: int = Field(description="User id")

class LoginResponce(BaseModel):
    token: str

@router.post("/register", response_model=UserSchemaResponce)
def register(user_data: UserSchema = Body()):
    repo = UserRepo(session = next(db.session))
    try:
        user = repo.save(
            CreateUserDTO(name=user_data.name, password=user_data.password)
        )
    except RepoError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return JSONResponse(content=jsonable_encoder(user))

@router.post("/login", response_model=LoginResponce)
def login(user_data: UserSchema = Body()):
    repo = UserRepo(session = next(db.session))
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
def me(authorization: Union[str, None] = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Token not found")
    try:
        user_id = auth_service.get_user_id(token=authorization)
        repo = UserRepo(session = next(db.session))
        user = repo.get(id=user_id)
    except (AuthError, RepoError) as err:
        raise HTTPException(status_code=401, detail=str(err))
    if not user:
        raise HTTPException(status_code=404, detail="User not found, probably deleted")
    return JSONResponse(content=jsonable_encoder(user))

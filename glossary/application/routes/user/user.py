from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from glossary.application.utils import auth_user, get_user_repo
from glossary.src.core.services.jwt_auth import auth_service

from glossary.src.core.entity.base import User
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.exception.base import AuthError, RepoError
from glossary.src.core.interfaces.repo.iuser_sql_repo import IUserSQLRepo

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

class UserSchema(BaseModel):
    login: str = Field(max_length=30, min_length=5)
    password: str = Field(max_length=30, min_length=5)

class UserSchemaResponce(UserSchema):
    id: int
    created_at: int

class LoginResponce(BaseModel):
    token: str

@router.post(
    "/register",
    response_model=UserSchemaResponce
)
def register(
    user_data: UserSchema = Body(),
    repo: IUserSQLRepo = Depends(get_user_repo)
):
    try:
        user = repo.save_user(
            CreateUserDTO(login=user_data.login, password=user_data.password)
        )
    except RepoError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return JSONResponse(content=jsonable_encoder(user))

@router.post(
    "/login",
    response_model=LoginResponce
)
def login(
    user_data: UserSchema = Body(),
    repo: IUserSQLRepo = Depends(get_user_repo)
):
    try:
        token = auth_service.login(
            login=user_data.login,
            password=user_data.password,
            repo=repo
        )
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))
    return JSONResponse(content=jsonable_encoder(LoginResponce(token=token)))

@router.get(
    "/me",
    response_model=UserSchemaResponce
)
def me(user: User = Depends(auth_user)):
    return JSONResponse(content=jsonable_encoder(user))

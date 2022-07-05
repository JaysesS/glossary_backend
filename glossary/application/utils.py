from datetime import datetime
import logging
from typing import Type, Union
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from glossary.application.database.holder import db
from glossary.application.routes.schemas import FailSchema
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import AuthError, RepoError
from glossary.src.core.interfaces.repo.iuser_sql_repo import IUserSQLRepo
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.usecases.result_base import Success, Fail
from glossary.src.data.glossary_repo.sql_repo.repo import GlossarySQLRepo
from glossary.src.core.services.jwt_auth import auth_service
from glossary.src.data.user_repo.sql_repo.repo import UserSQLRepo

from dataclasses import asdict

def init_debug_validation_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        logging.error(f"{request}: {exc_str}")
        content = {'message': exc_str}
        return JSONResponse(
            content=content, 
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


auth_scheme = HTTPBearer()

def convert_datetime_to_str(dt: datetime) -> str:
    return dt.strftime('%d.%m.%Y %H:%M:%S')

def reponse_from_result(response_model: Type[BaseModel], result: Union[Success, Fail]):
    if isinstance(result, Success):
        code = status.HTTP_200_OK
    elif isinstance(result, Fail):
        code = status.HTTP_400_BAD_REQUEST
    else:
        code = status.HTTP_501_NOT_IMPLEMENTED
    
    if code != status.HTTP_200_OK:
        response_model = FailSchema
    print(response_model, result)
    model = response_model(**asdict(result))
    return model, code

def status_code_by_type_result(result):
    if isinstance(result, Success):
        return status.HTTP_200_OK
    elif isinstance(result, Fail):
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_501_NOT_IMPLEMENTED

def get_glossary_repo() -> IGlossarySQLRepo:
    repo = GlossarySQLRepo(session = next(db.session))
    return repo

def get_user_repo() -> IUserSQLRepo:
    repo = UserSQLRepo(session = next(db.session))
    return repo


def auth_user(
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    repo: IUserSQLRepo = Depends(get_user_repo)
) -> User:
    try:
        user_id = auth_service.get_user_id(token=authorization.credentials)
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))
    
    try:
        user = repo.get_user(id=user_id)
    except RepoError as err:
        raise HTTPException(status_code=500, detail=str(err))

    if not user:
        raise HTTPException(status_code=404, detail="User not found, probably deleted")
    return user

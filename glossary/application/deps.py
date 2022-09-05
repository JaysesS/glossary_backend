from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.database.holder import db
from glossary.src.core.schemas.entity import UserSchema
from glossary.src.core.services.jwt_auth import auth_service
from glossary.src.data.crud.holder import user_crud

auth_scheme = HTTPBearer()

async def get_session() -> AsyncSession: # type: ignore
    async with db.session() as session: # type: ignore
        yield session

async def auth_user(
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    payload = auth_service.verify_token(
        token=authorization.credentials
    )
    user_id = payload["user_id"]
    user = await user_crud.get(
        session,
        id=user_id
    )
    return UserSchema(**user.__dict__)

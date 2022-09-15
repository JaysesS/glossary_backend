from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import auth_user, get_session
from glossary.application.routes.schemas import HTTPErrorSchema
from glossary.application.routes.user.schemas import TokenSchema, LoginSchema
from glossary.src.core.schemas.entity import UserSchema, UserCreateSchema
from glossary.src.core.services.jwt_auth import auth_service
from glossary.src.core.exception.base import AuthError
from glossary.src.data.crud.holder import user_crud


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post(
    "/register",
    responses={
        200: {"model": UserSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def user_register(
    data: UserCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    user = await user_crud.save(
        session,
        obj_in=data
    )
    return user

@router.post(
    "/login",
    responses={
        200: {"model": TokenSchema},
        401: {"model": HTTPErrorSchema}
    }
)
async def user_login(
    data: LoginSchema,
    session: AsyncSession = Depends(get_session),
):
    user = await user_crud.get_by_login(
        session,
        login=data.login
    )
    if user is None or user.password != data.password:
        raise AuthError("Invalid credentials")
    token = auth_service.generate_token(
        user_id=user.id
    )
    return JSONResponse(content=dict(token=token), status_code=status.HTTP_200_OK)


@router.get(
    "/me",
    responses={
        200: {"model": UserSchema},
        401: {"model": HTTPErrorSchema}
    }
)
async def user_me(
    user: UserSchema = Depends(auth_user),
):
    return user

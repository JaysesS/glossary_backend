from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import get_session
from glossary.application.routes.schemas import HTTPErrorSchema
from glossary.src.core.exception.base import CrudNotFoundError
from glossary.src.core.schemas.entity import UserSchema
from glossary.src.data.crud.holder import user_crud



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get(
    "/{id}",
    response_model=UserSchema,
    responses={
        200: {"model": UserSchema},
        404: {"model": HTTPErrorSchema}
    }
)
async def get_user(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        c = await user_crud.get(session, id=id)
    except CrudNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.msg)
    return c


# class UserSchema(BaseModel):
#     login: str = Field(max_length=30, min_length=5)
#     password: str = Field(max_length=30, min_length=5)

# class UserSchemaResponce(UserSchema):
#     id: int
#     created_at: int

# class LoginResponce(BaseModel):
#     token: str

# @router.post(
#     "/register",
#     response_model=UserSchemaResponce
# )
# def register(
#     user_data: UserSchema = Body(),
#     repo: IUserSQLRepo = Depends(get_user_repo)
# ):
#     try:
#         user = repo.save_user(
#             CreateUserDTO(login=user_data.login, password=user_data.password)
#         )
#     except RepoError as err:
#         raise HTTPException(status_code=400, detail=str(err))
#     return JSONResponse(content=jsonable_encoder(user))

# @router.post(
#     "/login",
#     response_model=LoginResponce
# )
# def login(
#     user_data: UserSchema = Body(),
#     repo: IUserSQLRepo = Depends(get_user_repo)
# ):
#     try:
#         token = auth_service.login(
#             login=user_data.login,
#             password=user_data.password,
#             repo=repo
#         )
#     except AuthError as err:
#         raise HTTPException(status_code=401, detail=str(err))
#     return JSONResponse(content=jsonable_encoder(LoginResponce(token=token)))

# @router.get(
#     "/me",
#     response_model=UserSchemaResponce
# )
# def me(user: User = Depends(auth_user)):
#     return JSONResponse(content=jsonable_encoder(user))

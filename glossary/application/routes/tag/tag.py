from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import auth_user, get_session
from glossary.application.routes.schemas import DeletedSchema, HTTPErrorSchema
from glossary.application.routes.tag.schemas import ListTagSchema, AppTagCreateSchema
from glossary.src.core.schemas.entity import UserSchema, TagSchema, TagCreateSchema, TagUpdateSchema
from glossary.src.data.crud.holder import tag_crud


router = APIRouter(
    prefix="/tag",
    tags=["Tag"]
)

@router.post(
    "/",
    responses={
        200: {"model": TagSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def tag_create(
    data: AppTagCreateSchema,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    tag_data = TagCreateSchema(
        user_id=user.id, name=data.name, description=data.description
    )
    tag = await tag_crud.save(
        session,
        obj_in=tag_data
    )
    return tag

@router.patch(
    "/",
    responses={
        200: {"model": TagSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def tag_update(
    data: TagUpdateSchema,
    _ = Depends(auth_user), # just for auth
    session: AsyncSession = Depends(get_session),
):
    tag = await tag_crud.update(
        session,
        obj_in=data
    )
    return tag

@router.delete(
    "/{id:int}",
    responses={
        200: {"model": DeletedSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def tag_delete(
    id: int,
    _ = Depends(auth_user), # just for auth
    session: AsyncSession = Depends(get_session),
):
    rm_id = await tag_crud.delete(
        session,
        id=id
    )
    return DeletedSchema(id=rm_id)

@router.get(
    "/list",
    responses={
        200: {"model": ListTagSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def tag_list(
    offset: int = 0, 
    limit: int = 100,
    _ = Depends(auth_user), # just for auth
    session: AsyncSession = Depends(get_session),
):
    tag_list = await tag_crud.get_many(
        session,
        limit=limit,
        offset=offset
    )
    return ListTagSchema(items=tag_list)


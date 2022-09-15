from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import auth_user, get_session
from glossary.application.routes.schemas import DeletedSchema, HTTPErrorSchema
from glossary.application.routes.word.schemas import ListWordSchema, AppWordCreateSchema
from glossary.src.core.schemas.entity import UserSchema, WordSchema, WordCreateSchema, WordUpdateSchema
from glossary.src.data.crud.holder import word_crud


router = APIRouter(
    prefix="/word",
    tags=["Word"]
)

@router.get(
    "/",
    responses={
        200: {"model": WordSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def word_get(
    id: int,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    word = await word_crud.get(
        session,
        id=id,
        user_id=user.id
    )
    return word

@router.post(
    "/",
    responses={
        200: {"model": WordSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def word_create(
    data: AppWordCreateSchema,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    word_data = WordCreateSchema(
        user_id=user.id, name=data.name,
        description=data.description,
        priority_id=data.priority_id
    )
    word = await word_crud.save(
        session,
        obj_in=word_data
    )
    return word

@router.patch(
    "/",
    responses={
        200: {"model": WordSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def word_update(
    data: WordUpdateSchema,
    user = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    word = await word_crud.update(
        session,
        obj_in=data,
        user_id=user.id
    )
    return word

@router.delete(
    "/{id:int}",
    responses={
        200: {"model": DeletedSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def word_delete(
    id: int,
    user = Depends(auth_user), 
    session: AsyncSession = Depends(get_session),
):
    rm_id = await word_crud.delete(
        session,
        id=id,
        user_id=user.id
    )
    return DeletedSchema(id=rm_id)

@router.get(
    "/list",
    responses={
        200: {"model": ListWordSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def word_list(
    offset: int = 0, 
    limit: int = 100,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    word_list = await word_crud.get_many(
        session,
        user_id=user.id,
        limit=limit,
        offset=offset
    )
    return ListWordSchema(items=word_list)


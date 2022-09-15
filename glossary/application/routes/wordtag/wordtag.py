from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.deps import auth_user, get_session
from glossary.application.routes.schemas import DeletedSchema, HTTPErrorSchema
from glossary.application.routes.wordtag.schemas import AppWordTagCreateSchema, ListWordTagSchema
from glossary.src.core.schemas.entity import UserSchema, WordTagSchema, WordTagCreateSchema
from glossary.src.data.crud.holder import word_crud, wordtag_crud


router = APIRouter(
    prefix="/link",
    tags=["Link"]
)

@router.post(
    "/",
    responses={
        200: {"model": WordTagSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def wordtag_create(
    data: AppWordTagCreateSchema,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    word_tag = await wordtag_crud.save(
        session,
        obj_in=WordTagCreateSchema(
            word_id=data.word_id,
            tag_id=data.tag_id,
            user_id=user.id
        )
    )
    return word_tag

@router.get(
    "/list",
    responses={
        200: {"model": ListWordTagSchema},
        400: {"model": HTTPErrorSchema}
    }
)
async def wordtag_list(
    offset: int = 0, 
    limit: int = 100,
    user: UserSchema = Depends(auth_user),
    session: AsyncSession = Depends(get_session),
):
    wordtag_list = await wordtag_crud.get_many(
        session,
        user_id=user.id,
        limit=limit,
        offset=offset
    )
    return ListWordTagSchema(items=wordtag_list)
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.src.data.crud.base import CRUDAsync, CRUDAsyncUserRequiredBase
from glossary.src.core.exception.base import CrudError, CrudNotFoundError
from glossary.src.data.models import UserModel, TagModel, WordModel, PriorityModel, WordTagModel
from glossary.src.core.schemas.entity import (
    UserSchema, UserCreateSchema, UserUpdateSchema,
    TagSchema, TagCreateSchema, TagUpdateSchema,
    WordSchema, WordCreateSchema, WordUpdateSchema,
    WordTagSchema, WordTagCreateSchema,
    PrioritySchema, PriorityCreateSchema,
)

class UserCRUD(CRUDAsync[UserModel, UserSchema, UserCreateSchema, UserUpdateSchema]):

    async def get_by_login(self, session: AsyncSession, *, login: str) -> Optional[UserSchema]:
        stmt = select(self.model).where(
            self.model.login == login
        )
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        if db_obj is None:
            raise CrudNotFoundError(f"Not found user with login={login}")
        return UserSchema(**db_obj.__dict__)

user_crud = UserCRUD(UserModel, UserSchema)

class PriorityCRUD(CRUDAsync[PriorityModel, PrioritySchema, PriorityCreateSchema, None]):
    """ """

priority_crud = PriorityCRUD(PriorityModel, PrioritySchema)

class TagCRUD(CRUDAsyncUserRequiredBase[TagModel, TagSchema, TagCreateSchema, TagUpdateSchema]):
    """ """

tag_crud = TagCRUD(TagModel, TagSchema)

class WordCRUD(CRUDAsyncUserRequiredBase[WordModel, WordSchema, WordCreateSchema, WordUpdateSchema]):
    """ """

word_crud = WordCRUD(WordModel, WordSchema)

class WordTagCRUD(CRUDAsyncUserRequiredBase[WordTagModel, WordTagSchema, WordTagCreateSchema, None]):

    async def save(
        self, session: AsyncSession, *, obj_in: WordTagCreateSchema
    ) -> Optional[WordTagSchema]:
        stmt = select(
            WordModel.id, TagModel.id
        ).join(
            TagModel, and_(WordModel.user_id == TagModel.user_id)
        ).where(
            and_(
                WordModel.id == obj_in.word_id,
                TagModel.id == obj_in.tag_id,
                WordModel.user_id == obj_in.user_id,
                TagModel.user_id == obj_in.user_id,
            )
        )
        coro = await session.execute(stmt)
        obj = coro.first()
        if obj is None:
            raise CrudError("Word or Tag not found")
        db_obj = WordTagModel(
            word_id=obj_in.word_id, tag_id=obj_in.tag_id, user_id=obj_in.user_id
        )
        session.add(db_obj)
        try:
            await session.flush()
        except Exception:
            await session.rollback()
            raise CrudError("Error on save")
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

wordtag_crud = WordTagCRUD(WordTagModel, WordTagSchema)
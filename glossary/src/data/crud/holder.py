from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.src.data.crud.base import CRUDASyncBase
from glossary.src.core.exception.base import CrudNotFoundError
from glossary.src.data.models import UserModel, TagModel, WordModel, PriorityModel, WordTagModel
from glossary.src.core.schemas.entity import (
    UserSchema, UserCreateSchema, UserUpdateSchema,
    TagSchema, TagCreateSchema, TagUpdateSchema,
    WordSchema, WordCreateSchema, WordUpdateSchema,
    PrioritySchema, PriorityCreateSchema,
)

class UserCRUD(CRUDASyncBase[UserModel, UserSchema, UserCreateSchema, UserUpdateSchema]):

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

class PriorityCRUD(CRUDASyncBase[PriorityModel, PrioritySchema, PriorityCreateSchema, None]):
    """ Declare model specific CRUD operation methods. """

priority_crud = PriorityCRUD(PriorityModel, PrioritySchema)

class TagCRUD(CRUDASyncBase[TagModel, TagSchema, TagCreateSchema, TagUpdateSchema]):
    """ Declare model specific CRUD operation methods. """

tag_crud = TagCRUD(TagModel, TagSchema)

class WordCRUD(CRUDASyncBase[WordModel, WordSchema, WordCreateSchema, WordUpdateSchema]):
    """ Declare model specific CRUD operation methods. """

word_crud = WordCRUD(WordModel, WordSchema)
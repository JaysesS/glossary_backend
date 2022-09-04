import sqlalchemy
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, List, Optional, Type

from glossary.src.core.exception.base import CrudError, CrudNotFoundError
from glossary.src.core.interfaces.crud import ICRUDASyncBase, CreateSchemaType, ModelType, UpdateSchemaType


class CRUDASyncBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ICRUDASyncBase):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, *, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == id
        )
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        if db_obj is None:
            raise CrudNotFoundError(f"Not found user with id={id}")
        return db_obj

    async def get_many(self, session: AsyncSession, *, offset: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        coro = await session.execute(stmt)
        db_obj_list = coro.scalars()
        return db_obj_list

    async def save(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def update(self, session: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = db_obj.to_dict()
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def delete(self, session: AsyncSession, *, id: int) -> Optional[int]:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        c = await session.execute(stmt)
        try:
            rm_id, = c.one()
        except sqlalchemy.exc.NoResultFound:
            raise CrudError("Entity not found")
        await session.commit()
        return rm_id
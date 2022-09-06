import sqlalchemy
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, List, Optional, Type

from glossary.src.core.exception.base import CrudError
from glossary.src.core.interfaces.crud import ICRUDASyncBase, EntitySchemaType, CreateSchemaType, ModelType, UpdateSchemaType


class CRUDASyncBase(
    Generic[ModelType, EntitySchemaType, CreateSchemaType, UpdateSchemaType],
    ICRUDASyncBase
):

    def __init__(self, model: Type[ModelType], entity_schema: Type[EntitySchemaType]):
        self.model = model
        self.entity_schema = entity_schema

    async def get(self, session: AsyncSession, *, id: int) -> Optional[EntitySchemaType]:
        stmt = select(self.model).where(
            self.model.id == id
        )
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        if db_obj is None:
            return None
        return self.entity_schema(**db_obj.__dict__)

    async def get_many(
        self, session: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> List[EntitySchemaType]:
        stmt = select(self.model).offset(offset).limit(limit)
        coro = await session.execute(stmt)
        db_obj_list = coro.scalars()
        return [self.entity_schema(**obj.__dict__) for obj in db_obj_list]

    async def save(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> EntitySchemaType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        try:
            await session.flush()
        except Exception as e:
            await session.rollback()
            raise CrudError("Error on save")
        await session.commit()
        await session.refresh(db_obj)
        return self.entity_schema(**db_obj.__dict__)

    async def update(self, session: AsyncSession, *, obj_in: UpdateSchemaType) -> EntitySchemaType:
        stmt = select(self.model).where(
            self.model.id == obj_in.id # type: ignore
        )
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        if db_obj is None:
            raise CrudError("Not found")
        update_data = obj_in.dict(exclude={'id'}, exclude_unset=True) # type: ignore
        obj_data = db_obj.__dict__
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return self.entity_schema(**db_obj.__dict__)

    async def delete(self, session: AsyncSession, *, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        c = await session.execute(stmt)
        try:
            rm_id, = c.one()
        except sqlalchemy.exc.NoResultFound:  # type: ignore
            raise CrudError("Not found")
        await session.commit()
        return rm_id
import sqlalchemy
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, List, Optional, Type
from sqlalchemy.sql.selectable import Select
from glossary.src.core.exception.base import CrudError
from glossary.src.core.interfaces.crud import ICRUDASync, ICRUDASyncUserRequired, EntitySchemaType, CreateSchemaType, ModelType, UpdateSchemaType

class CRUDStmtBase:

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, *, id: int) -> Select:
        stmt = select(self.model).where(self.model.id==id)
        return stmt

    def get_many(
        self, *, offset: int = 0, limit: int = 100
    ) -> Select:
        stmt = select(self.model).offset(offset).limit(limit)
        return stmt

    def delete(self, *, id: int) -> Select:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        return stmt

class CRUDExecuteBase(Generic[EntitySchemaType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, entity_schema: Type[EntitySchemaType], model: Type[ModelType]):
        self.entity_schema = entity_schema
        self.model = model

    async def get(self, session: AsyncSession, *, stmt: Select) -> Optional[EntitySchemaType]:
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        if db_obj is None:
            raise CrudError("Not found")
        return self.entity_schema(**db_obj.__dict__)

    async def get_many(
        self, session: AsyncSession, *, stmt: Select
    ) -> List[EntitySchemaType]:
        coro = await session.execute(stmt)
        db_obj_list = coro.scalars()
        return [self.entity_schema(**obj.__dict__) for obj in db_obj_list]

    async def update(self, session: AsyncSession, *, stmt: Select) -> EntitySchemaType:
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

    async def delete(self, session: AsyncSession, *, stmt: Select) -> int:
        c = await session.execute(stmt)
        try:
            rm_id, = c.one()
        except sqlalchemy.exc.NoResultFound:  # type: ignore
            raise CrudError("Not found")
        await session.commit()
        return rm_id


class CRUDAsync(
    ICRUDASync,
    Generic[ModelType, EntitySchemaType, CreateSchemaType, UpdateSchemaType]
):

    def __init__(self, model: Type[ModelType], entity_schema: Type[EntitySchemaType]):
        self.model = model
        self.entity_schema = entity_schema
        self._stmt = CRUDStmtBase(self.model)
        self._execute = CRUDExecuteBase(self.entity_schema, self.model)

    async def get(self, session: AsyncSession, *, id: int) -> Optional[EntitySchemaType]:
        stmt = self._stmt.get(id=id)
        return await self._execute.get(session, stmt=stmt)

    async def get_many(
        self, session: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> List[EntitySchemaType]:
        stmt = self._stmt.get_many(offset=offset, limit=limit)
        return await self._execute.get_many(session, stmt=stmt)

    async def update(self, session: AsyncSession, *, obj_in: UpdateSchemaType) -> EntitySchemaType:
        stmt = self._stmt.get(id=obj_in.id) # type: ignore
        return await self._execute.update(session, stmt=stmt)

    async def save(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> EntitySchemaType:
        return await self._execute.save(session, obj_in=obj_in)

    async def delete(self, session: AsyncSession, *, id: int) -> int:
        stmt = self._stmt.delete(id=id)
        return await self._execute.delete(session, stmt=stmt)

class CRUDAsyncUserRequiredBase(
    ICRUDASyncUserRequired,
    Generic[ModelType, EntitySchemaType, CreateSchemaType, UpdateSchemaType],
):

    def __init__(self, model: Type[ModelType], entity_schema: Type[EntitySchemaType]):
        self.model = model
        self.entity_schema = entity_schema
        self._stmt = CRUDStmtBase(self.model)
        self._execute = CRUDExecuteBase(self.entity_schema, self.model)

    async def get(self, session: AsyncSession, *, id: int, user_id: int) -> Optional[EntitySchemaType]:
        stmt = self._stmt.get(id=id).where(self.model.user_id==user_id)
        return await self._execute.get(session, stmt=stmt)

    async def get_many(
        self, session: AsyncSession, *, user_id: int, offset: int = 0, limit: int = 100
    ) -> List[EntitySchemaType]:
        stmt = self._stmt.get_many(offset=offset, limit=limit).where(self.model.user_id==user_id)
        return await self._execute.get_many(session, stmt=stmt)

    async def update(self, session: AsyncSession, *, user_id: int, obj_in: UpdateSchemaType) -> EntitySchemaType:
        stmt = self._stmt.get(id=obj_in.id).where(self.model.user_id==user_id) # type: ignore
        return await self._execute.update(session, stmt=stmt)

    async def save(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> EntitySchemaType:
        return await self._execute.save(session, obj_in=obj_in)

    async def delete(self, session: AsyncSession, *, user_id: int, id: int) -> int:
        stmt = self._stmt.delete(id=id).where(self.model.user_id==user_id)
        return await self._execute.delete(session, stmt=stmt)

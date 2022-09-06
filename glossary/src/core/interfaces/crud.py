from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from glossary.application.database.holder import Base

ModelType = TypeVar("ModelType", bound=Base)
EntitySchemaType = TypeVar("EntitySchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Optional[BaseModel])

class ICRUDASyncBase(ABC):

    @abstractmethod
    async def get(
        self, session: AsyncSession, *, id: int
    ) -> Optional[EntitySchemaType]:
        pass

    @abstractmethod
    async def get_many(
        self, session: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> List[EntitySchemaType]:
        pass

    @abstractmethod
    async def save(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> EntitySchemaType:
        pass

    @abstractmethod
    async def update(
        self, session: AsyncSession, *, db_obj: ModelType, obj_in: EntitySchemaType
    ) -> ModelType:
        pass

    @abstractmethod
    async def delete(
        self, session: AsyncSession, *, id: int
    ) -> int:
        pass

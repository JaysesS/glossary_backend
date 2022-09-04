from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:

    def __init__(self) -> None:
        self._engine = None

    def configure(self, url: str):
        self._engine = create_async_engine(url)
    
    @property
    def session(self):
        return sessionmaker(
            bind=self._engine, class_=AsyncSession, autocommit=False, autoflush=False,
        )

Base = declarative_base()
db = Database()

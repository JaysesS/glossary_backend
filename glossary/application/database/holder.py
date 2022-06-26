from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:

    def __init__(self) -> None:
        self._database_url: Optional[str] = None
        self._engine = None

    @property
    def url(self):
        return self._database_url
    
    @url.setter
    def url(self, url: str):
        self._database_url = url
    
    @property
    def session(self):
        s = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)()
        try:
            yield s
        finally:
            s.close()
    
    def make_engine(self):
        if self._database_url is None:
            raise Exception("Database url not set!")

        self._engine = create_engine(self._database_url)

Base = declarative_base()
db = Database()


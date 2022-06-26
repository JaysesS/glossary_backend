from glossary.application.database.holder import Base
from sqlalchemy import Column, Integer, String


class TagModel(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

from glossary.application.database.holder import Base
from sqlalchemy import Column, Integer, String


class PriorityModel(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


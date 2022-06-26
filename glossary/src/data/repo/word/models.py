from glossary.application.database.holder import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class WordModel(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    priority_id = Column(Integer, ForeignKey("priority.id"))
    tags = relationship("Tag", back_populates="word")

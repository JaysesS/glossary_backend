from glossary.application.database.holder import Base
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from glossary.src.data.glossary_repo.models import WordModel

class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=func.now())
    words = relationship("WordModel", cascade="all,delete", back_populates="user")
from glossary.application.database.holder import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)

    words = relationship("Word", back_populates="user")
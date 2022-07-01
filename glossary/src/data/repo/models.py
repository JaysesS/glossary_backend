from glossary.application.database.holder import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class TagModel(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    words = relationship("WordModel", secondary='word_tags', back_populates="tags")

class WordModel(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    priority_id = Column(Integer, ForeignKey("priority.id"))
    tags = relationship('TagModel', secondary='word_tags', back_populates='words')
    user = relationship('UserModel')
    user_id = Column(Integer, ForeignKey('user.id'))


class WordTagModel(Base):
    __tablename__ = "word_tags"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    words = relationship("WordModel", back_populates="user")

class PriorityModel(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
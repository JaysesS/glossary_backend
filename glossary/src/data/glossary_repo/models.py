from glossary.application.database.holder import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

class PriorityModel(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class TagModel(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    words = relationship("WordModel", secondary='word_tags', back_populates="tags")

class WordModel(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=func.now())
    priority_id = Column(Integer, ForeignKey("priority.id"))
    priority = relationship("PriorityModel", foreign_keys=[priority_id])
    tags = relationship('TagModel', secondary='word_tags', back_populates='words')
    user = relationship('UserModel')
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))


class WordTagModel(Base):
    __tablename__ = "word_tags"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id', ondelete="CASCADE",))
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete="CASCADE",))

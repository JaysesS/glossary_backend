from sqlalchemy import Column, ForeignKey, Integer, String, func

from glossary.application.database.holder import Base
from glossary.src.data.mixin import TimeMixin

class UserModel(TimeMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True)
    password = Column(String)

class PriorityModel(TimeMixin, Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class TagModel(TimeMixin, Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))

class WordModel(TimeMixin, Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    priority_id = Column(Integer, ForeignKey("priority.id"))
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))


class WordTagModel(TimeMixin, Base):
    __tablename__ = "word_tags"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('word.id', ondelete="CASCADE",))
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete="CASCADE",))

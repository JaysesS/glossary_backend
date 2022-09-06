from typing import Optional
from pydantic import BaseModel

from glossary.src.core.schemas.mixin import TimeMixin

"""
    User
"""
class UserSchema(TimeMixin, BaseModel):
    id: int
    login: str
    password: str

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    login: str
    password: str

class UserUpdateSchema(BaseModel):
    password: str


"""
    Priority
"""
class PrioritySchema(TimeMixin, BaseModel):
    id: int
    name: str

class PriorityCreateSchema(BaseModel):
    name: str


"""
    Tag
"""
class TagSchema(TimeMixin, BaseModel):
    id: int
    name: str
    description: str

class TagCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int

class TagUpdateSchema(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None


"""
    Word
"""
class WordSchema(TimeMixin, BaseModel):
    id: int
    name: str
    description: str
    priority_id: int

class WordCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    priority_id: int
    user_id: int

class WordUpdateSchema(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    priority_id: Optional[int] = None

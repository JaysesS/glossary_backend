from dataclasses import dataclass
from typing import List
from glossary.src.core.entity.base import Priority, Tag

@dataclass
class CreateTagDTO:
    name: str
    description: str

@dataclass
class UpdateTagDTO:
    id: int
    description: str

@dataclass
class CreateWordDTO:
    name: str
    description: str
    tags: List[Tag]
    priority: Priority

@dataclass
class UpdateWordDTO:
    id: int
    description: str
    tag_ids: List[int]
    priority_id: int

@dataclass
class CreateUserDTO:
    name: str
    password: str
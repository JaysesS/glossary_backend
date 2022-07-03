from dataclasses import dataclass
from typing import List, Optional
from glossary.src.core.entity.base import Priority, Tag

@dataclass
class CreateTagDTO:
    name: str
    description: str

@dataclass
class UpdateTagDTO:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class CreateWordDTO:
    name: str
    description: str
    tag_ids: List[int]
    priority_id: int

@dataclass
class UpdateWordDTO:
    id: int
    description: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    priority_id: Optional[int] = None

@dataclass
class CreateUserDTO:
    name: str
    password: str

@dataclass
class CreatePriorityDTO:
    name: str

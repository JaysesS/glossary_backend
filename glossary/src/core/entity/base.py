from dataclasses import dataclass
from typing import List


@dataclass
class Priority:
    id: int
    name: str

@dataclass
class Tag:
    id: int
    name: str
    description: str
    created_at: int

@dataclass
class Word:
    id: int
    name: str
    description: str
    tags: List[Tag]
    priority: Priority
    created_at: int

@dataclass
class User:
    id: int
    login: str
    password: str
    created_at: int
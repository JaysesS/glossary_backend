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

@dataclass
class Word:
    id: int
    name: str
    description: str
    tags: List[Tag]
    priority: Priority

@dataclass
class User:
    id: int
    name: str
    password: str
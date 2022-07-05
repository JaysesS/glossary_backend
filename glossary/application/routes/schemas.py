from typing import List
from pydantic import BaseModel, Field

class FailSchema(BaseModel):
    msg: str

class PriorirySchema(BaseModel):
    id: int
    name: str

class TagSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: int

class WordSchema(BaseModel):
    id: int
    name: str = Field(min_length=1)
    description: str = Field(min_length=0)
    tags: List[TagSchema]
    priority: PriorirySchema
    created_at: int
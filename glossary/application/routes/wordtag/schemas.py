from pydantic import BaseModel
from typing import List

from glossary.src.core.schemas.entity import WordTagSchema

class ListWordTagSchema(BaseModel):
    items: List[WordTagSchema]

class AppWordTagCreateSchema(BaseModel):
    word_id: int
    tag_id: int
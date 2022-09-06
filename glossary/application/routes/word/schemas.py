from pydantic import BaseModel
from typing import Optional, List

from glossary.src.core.schemas.entity import WordSchema

class ListWordSchema(BaseModel):
    items: List[WordSchema]

class AppWordCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    priority_id: int
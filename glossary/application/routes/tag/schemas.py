from pydantic import BaseModel
from typing import Optional, List

from glossary.src.core.schemas.entity import TagSchema

class ListTagSchema(BaseModel):
    items: List[TagSchema]

class AppTagCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

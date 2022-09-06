from pydantic import BaseModel
from typing import List

from glossary.src.core.schemas.entity import PrioritySchema

class ListPrioritySchema(BaseModel):
    items: List[PrioritySchema]

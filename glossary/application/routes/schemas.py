from typing import List
from pydantic import BaseModel, Field

class HTTPErrorSchema(BaseModel):
    detail: str

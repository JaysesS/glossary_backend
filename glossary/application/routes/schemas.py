from pydantic import BaseModel

class HTTPErrorSchema(BaseModel):
    detail: str

class DeletedSchema(BaseModel):
    id: int
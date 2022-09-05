from pydantic import BaseModel

class TokenSchema(BaseModel):
    token: str

class LoginSchema(BaseModel):
    login: str
    password: str

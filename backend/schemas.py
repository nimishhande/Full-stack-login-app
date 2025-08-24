from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str | None
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

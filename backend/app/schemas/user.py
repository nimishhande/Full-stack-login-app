import uuid
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: str
    provider: str

    class Config:
        from_attributes = True

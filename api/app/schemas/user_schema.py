from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.models.user import RoleEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.customer

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

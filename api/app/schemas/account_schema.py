from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class AccountCreate(BaseModel):
    initial_deposit: float = Field(default=0.0, ge=0.0)

class AccountResponse(BaseModel):
    id: UUID
    account_number: str
    balance: float
    status: str

    class Config:
        from_attributes = True

class AccountUpdate(BaseModel):
    status: str

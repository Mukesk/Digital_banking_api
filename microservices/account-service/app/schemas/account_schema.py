from pydantic import BaseModel
from uuid import UUID

class AccountCreate(BaseModel):
    initial_balance: float = 0.0

class AccountResponse(BaseModel):
    id: UUID
    user_id: UUID
    account_number: str
    balance: float
    status: str

    class Config:
        from_attributes = True

class AccountUpdate(BaseModel):
    pass # Add fields if needed

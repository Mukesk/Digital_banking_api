from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    to_account_id: UUID
    amount: float

class TransactionResponse(BaseModel):
    id: UUID
    from_account_id: Optional[UUID]
    to_account_id: UUID
    amount: float
    type: str
    created_at: datetime

    class Config:
        from_attributes = True

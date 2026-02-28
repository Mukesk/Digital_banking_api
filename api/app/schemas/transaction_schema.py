from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class TransferRequest(BaseModel):
    to_account: str
    amount: float = Field(gt=0.0)

class TransactionResponse(BaseModel):
    id: UUID
    from_account: Optional[UUID]
    to_account: Optional[UUID]
    amount: float
    type: str # transfer, deposit, withdrawal
    created_at: datetime

    class Config:
        from_attributes = True

class TransferResponse(BaseModel):
    transaction_id: UUID
    status: str

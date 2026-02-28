from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class LoanApply(BaseModel):
    amount: float = Field(gt=0.0)

class LoanResponse(BaseModel):
    id: UUID
    user_id: UUID
    amount: float
    status: str
    interest_rate: Optional[float]

    class Config:
        from_attributes = True

class LoanApproveResponse(BaseModel):
    loan_id: UUID
    status: str

class LoanUpdate(BaseModel):
    interest_rate: float

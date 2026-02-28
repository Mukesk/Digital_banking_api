from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.loan_schema import LoanApply, LoanResponse
from app.services.loan_service import loan_service
from app.core.security import get_current_user

router = APIRouter()

@router.post("/apply", response_model=LoanResponse)
def apply_loan(data: LoanApply, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return loan_service.apply_loan(db, current_user["sub"], data.amount)

@router.put("/{id}/approve", response_model=LoanResponse)
def approve_loan(id: str, interest_rate: float = 5.0, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return loan_service.approve_loan(db, id, current_user.get("role"), interest_rate)

@router.put("/{id}/reject", response_model=LoanResponse)
def reject_loan(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return loan_service.reject_loan(db, id, current_user.get("role"))

@router.delete("/{id}")
def delete_loan(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return loan_service.delete_loan(db, id, current_user.get("role"))

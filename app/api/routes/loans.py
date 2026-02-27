from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.loan import Loan
from app.models.account import Account
from app.models.user import User, RoleEnum
from app.schemas.loan_schema import LoanApply, LoanResponse, LoanApproveResponse, LoanUpdate
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/apply", response_model=LoanApproveResponse, status_code=status.HTTP_201_CREATED)
def apply_loan(
    loan_in: LoanApply,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.customer.value))
):
    new_loan = Loan(
        user_id=current_user.id,
        amount=loan_in.amount,
        status="pending"
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return LoanApproveResponse(loan_id=new_loan.id, status=new_loan.status)

@router.get("", response_model=list[LoanResponse])
def get_user_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    # Customer can only see their own loans
    if current_user.role == RoleEnum.customer:
        return db.query(Loan).filter(Loan.user_id == current_user.id).offset(skip).limit(limit).all()
    # Officers/Admins can see all
    return db.query(Loan).offset(skip).limit(limit).all()

@router.put("/{loan_id}/approve", response_model=LoanApproveResponse)
def approve_loan(
    loan_id: UUID,
    db: Session = Depends(get_db),
    officer: User = Depends(require_role(RoleEnum.officer.value))
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending state")
        
    loan.status = "approved"
    
    # Disburse amount to active user account
    user_account = db.query(Account).filter(Account.user_id == loan.user_id, Account.status == "active").first()
    if user_account:
        user_account.balance += loan.amount
        
    db.commit()
    db.refresh(loan)
    return LoanApproveResponse(loan_id=loan.id, status=loan.status)

@router.put("/{loan_id}/reject", response_model=LoanApproveResponse)
def reject_loan(
    loan_id: UUID,
    db: Session = Depends(get_db),
    officer: User = Depends(require_role(RoleEnum.officer.value))
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    loan.status = "rejected"
    db.commit()
    db.refresh(loan)
    return LoanApproveResponse(loan_id=loan.id, status=loan.status)

@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: UUID,
    loan_in: LoanUpdate,
    db: Session = Depends(get_db),
    officer: User = Depends(require_role(RoleEnum.officer.value))
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    loan.interest_rate = loan_in.interest_rate
    db.commit()
    db.refresh(loan)
    return loan

@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(
    loan_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(RoleEnum.admin.value))
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
        
    db.delete(loan)
    db.commit()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.core.database import get_db
from app.models.user import User, RoleEnum
from app.models.account import Account
from app.models.loan import Loan
from app.models.transaction import Transaction
from app.core.dependencies import require_role

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/reports")
def get_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(RoleEnum.admin.value))
):
    total_accounts = db.query(func.count(Account.id)).scalar()
    total_loans = db.query(func.count(Loan.id)).scalar()
    
    today = datetime.utcnow().date()
    total_transactions_today = db.query(func.count(Transaction.id)).filter(
        func.date(Transaction.created_at) == today
    ).scalar()
    
    return {
        "total_accounts": total_accounts,
        "total_loans": total_loans,
        "total_transactions_today": total_transactions_today
    }

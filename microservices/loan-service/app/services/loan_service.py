from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.loan_repo import loan_repo
from app.events.producer import publish_event

class LoanService:
    def apply_loan(self, db: Session, user_id: str, amount: float):
        return loan_repo.create(db, user_id, amount)

    def approve_loan(self, db: Session, loan_id: str, role: str, interest_rate: float):
        if role != "officer":
            raise HTTPException(status_code=403, detail="Officer only")
        loan = loan_repo.update_status(db, loan_id, "approved", interest_rate)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        
        publish_event('loan.approved', {
            'loan_id': str(loan.id),
            'user_id': str(loan.user_id),
            'amount': loan.amount,
            'interest_rate': loan.interest_rate,
            'timestamp': loan.created_at.isoformat()
        })
        return loan

    def reject_loan(self, db: Session, loan_id: str, role: str):
        if role != "officer":
            raise HTTPException(status_code=403, detail="Officer only")
        loan = loan_repo.update_status(db, loan_id, "rejected")
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return loan

    def delete_loan(self, db: Session, loan_id: str, role: str):
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        loan = loan_repo.delete(db, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return {"message": "Loan deleted"}

loan_service = LoanService()

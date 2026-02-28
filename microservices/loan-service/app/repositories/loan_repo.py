from sqlalchemy.orm import Session
from app.models.loan import Loan

class LoanRepository:
    def create(self, db: Session, user_id: str, amount: float):
        loan = Loan(user_id=user_id, amount=amount)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    def get_by_id(self, db: Session, loan_id: str):
        return db.query(Loan).filter(Loan.id == loan_id).first()

    def update_status(self, db: Session, loan_id: str, status: str, interest_rate: float = None):
        loan = self.get_by_id(db, loan_id)
        if loan:
            loan.status = status
            if interest_rate is not None:
                loan.interest_rate = interest_rate
            db.commit()
            db.refresh(loan)
        return loan

    def delete(self, db: Session, loan_id: str):
        loan = self.get_by_id(db, loan_id)
        if loan:
            db.delete(loan)
            db.commit()
        return loan

loan_repo = LoanRepository()

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.account_repo import account_repo

class AccountService:
    def create_account(self, db: Session, user_id: str, initial_balance: float):
        return account_repo.create_account(db, user_id, initial_balance)

    def get_account(self, db: Session, account_id: str, user_id: str, role: str):
        account = account_repo.get_by_id(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if role != "admin" and str(account.user_id) != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        return account

    def freeze_account(self, db: Session, account_id: str, role: str):
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        account = account_repo.update_status(db, account_id, "frozen")
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def delete_account(self, db: Session, account_id: str, role: str):
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        account = account_repo.delete_account(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return {"message": "Account deleted successfully"}

account_service = AccountService()

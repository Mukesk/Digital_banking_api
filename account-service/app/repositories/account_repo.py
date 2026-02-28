from sqlalchemy.orm import Session
from app.models.account import Account

class AccountRepository:
    def create_account(self, db: Session, user_id: str, balance: float):
        new_account = Account(user_id=user_id, balance=balance)
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account

    def get_by_id(self, db: Session, account_id: str):
        return db.query(Account).filter(Account.id == account_id).first()
    
    def get_by_user_id_and_account_id(self, db: Session, user_id: str, account_id: str):
        return db.query(Account).filter(Account.user_id == user_id, Account.id == account_id).first()

    def update_status(self, db: Session, account_id: str, status: str):
        account = self.get_by_id(db, account_id)
        if account:
            account.status = status
            db.commit()
            db.refresh(account)
        return account

    def delete_account(self, db: Session, account_id: str):
        account = self.get_by_id(db, account_id)
        if account:
            db.delete(account)
            db.commit()
        return account
    
    def update_balance(self, db: Session, account_id: str, delta: float):
        account = self.get_by_id(db, account_id)
        if account:
            account.balance += delta
            db.commit()
            db.refresh(account)
        return account

account_repo = AccountRepository()

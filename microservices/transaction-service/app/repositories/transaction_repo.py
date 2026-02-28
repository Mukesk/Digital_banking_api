from sqlalchemy.orm import Session
from app.models.transaction import Transaction

class TransactionRepository:
    def create(self, db: Session, from_id: str, to_id: str, amount: float, txn_type: str = "transfer"):
        txn = Transaction(from_account_id=from_id, to_account_id=to_id, amount=amount, type=txn_type)
        db.add(txn)
        db.commit()
        db.refresh(txn)
        return txn

    def get_user_transactions(self, db: Session, account_ids: list[str]):
        return db.query(Transaction).filter(
            (Transaction.from_account_id.in_(account_ids)) | (Transaction.to_account_id.in_(account_ids))
        ).all()

    def get_all(self, db: Session):
        return db.query(Transaction).all()

    def delete(self, db: Session, txn_id: str):
        txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
        if txn:
            db.delete(txn)
            db.commit()
        return txn

transaction_repo = TransactionRepository()

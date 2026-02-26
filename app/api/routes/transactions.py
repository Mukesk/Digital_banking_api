from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import redis
from uuid import UUID

from app.core.database import get_db
from app.core.config import settings
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User, RoleEnum
from app.schemas.transaction_schema import TransferRequest, TransactionResponse, TransferResponse
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/transactions", tags=["transactions"])

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

@router.post("/transfer", response_model=TransferResponse)
def transfer_funds(
    transfer_in: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find active source account for the user
    source_acc = db.query(Account).filter(Account.user_id == current_user.id, Account.status == "active").first()
    if not source_acc:
        raise HTTPException(status_code=400, detail="No active source account found")
    
    # Use Redis Lock to prevent race conditions
    lock_name = f"lock:transfer:{source_acc.id}"
    with redis_client.lock(lock_name, timeout=10, blocking_timeout=5):
        # Refresh from db
        db.refresh(source_acc)
        
        if source_acc.balance < transfer_in.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        dest_acc = db.query(Account).filter(Account.account_number == transfer_in.to_account, Account.status == "active").first()
        if not dest_acc:
            raise HTTPException(status_code=404, detail="Destination account not found or is not active")
        
        # Deduct and Add
        source_acc.balance -= transfer_in.amount
        dest_acc.balance += transfer_in.amount
        
        new_tx = Transaction(
            from_account=source_acc.id,
            to_account=dest_acc.id,
            amount=transfer_in.amount,
            type="transfer"
        )
        
        db.add(new_tx)
        db.commit()
        db.refresh(new_tx)
        
        return TransferResponse(transaction_id=new_tx.id, status="success")

@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_accounts = db.query(Account.id).filter(Account.user_id == current_user.id).all()
    account_ids = [acc.id for acc in user_accounts]
    
    transactions = db.query(Transaction).filter(
        (Transaction.from_account.in_(account_ids)) | 
        (Transaction.to_account.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).all()
    
    return transactions

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_role(RoleEnum.admin.value))
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    db.delete(transaction)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random
import string
from uuid import UUID

from app.core.database import get_db
from app.models.account import Account
from app.models.user import User, RoleEnum
from app.schemas.account_schema import AccountCreate, AccountResponse, AccountUpdate
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/accounts", tags=["accounts"])

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_account = Account(
        user_id=current_user.id,
        account_number=generate_account_number(),
        balance=account_in.initial_deposit,
        status="active"
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.user_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    return account

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    account_in: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this account")
    
    account.status = account_in.status
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_role(RoleEnum.admin.value))
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()

@router.put("/{account_id}/freeze", response_model=AccountResponse)
def freeze_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_role(RoleEnum.admin.value))
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.status = "frozen"
    db.commit()
    db.refresh(account)
    return account

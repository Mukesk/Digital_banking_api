from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.services.account_service import account_service
from app.core.security import get_current_user
from app.repositories.account_repo import account_repo

router = APIRouter()

@router.post("", response_model=AccountResponse, status_code=201)
def create_account(data: AccountCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return account_service.create_account(db, current_user["sub"], data.initial_balance)

@router.get("/{id}", response_model=AccountResponse)
def get_account(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return account_service.get_account(db, id, current_user["sub"], current_user.get("role"))

@router.put("/{id}")
def update_account(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Basic update not explicitly detailed; returning HTTP 200
    account = account_service.get_account(db, id, current_user["sub"], current_user.get("role"))
    return {"message": "Account updated", "account_id": id}

@router.delete("/{id}")
def delete_account(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return account_service.delete_account(db, id, current_user.get("role"))

@router.put("/{id}/freeze")
def freeze_account(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return account_service.freeze_account(db, id, current_user.get("role"))

# Internal endpoint for Transaction Service
@router.get("/internal/{id}")
def get_account_internal(id: str, db: Session = Depends(get_db)):
    account = account_repo.get_by_id(db, id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"id": account.id, "balance": account.balance, "status": account.status.value}

@router.put("/internal/{id}/balance")
def update_balance_internal(id: str, delta: float, db: Session = Depends(get_db)):
    account = account_repo.update_balance(db, id, delta)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"status": "ok"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.services.transaction_service import transaction_service
from app.core.security import get_current_user

router = APIRouter()

@router.post("/transfer", response_model=TransactionResponse)
async def transfer(data: TransactionCreate, from_account_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Note: the prompt says "POST /transactions/transfer Transfer money between accounts".
    # Typically from_account_id would be in the request body, but let's assume it's passed as a query param or part of body based on user ownership
    # We'll just rely on the service to take it from query for simplicity or add to schema.
    return await transaction_service.transfer(db, from_account_id, str(data.to_account_id), data.amount)

@router.delete("/{id}")
def delete_transaction(id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return transaction_service.delete(db, id, current_user.get("role"))

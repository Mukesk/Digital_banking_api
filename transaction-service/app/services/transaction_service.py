import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.transaction_repo import transaction_repo
from app.core.redis_lock import acquire_lock, release_lock
from app.events.producer import publish_event
from app.core.config import settings

class TransactionService:
    async def transfer(self, db: Session, from_account_id: str, to_account_id: str, amount: float):
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Transfer amount must be positive")
        
        # Sort IDs to prevent deadlocks
        ids = sorted([str(from_account_id), str(to_account_id)])
        lock1 = acquire_lock(ids[0])
        lock2 = acquire_lock(ids[1])
        
        try:
            async with httpx.AsyncClient() as client:
                # 1. Fetch from_account
                from_resp = await client.get(f"{settings.ACCOUNT_SERVICE_URL}/accounts/internal/{from_account_id}")
                if from_resp.status_code != 200:
                    raise HTTPException(status_code=400, detail="Source account not found")
                from_data = from_resp.json()
                
                if from_data.get("status") == "frozen":
                    raise HTTPException(status_code=400, detail="Source account is frozen")
                if from_data.get("balance") < amount:
                    raise HTTPException(status_code=400, detail="Insufficient balance")

                # 2. Fetch to_account
                to_resp = await client.get(f"{settings.ACCOUNT_SERVICE_URL}/accounts/internal/{to_account_id}")
                if to_resp.status_code != 200:
                    raise HTTPException(status_code=400, detail="Destination account not found")
                if to_resp.json().get("status") == "frozen":
                    raise HTTPException(status_code=400, detail="Destination account is frozen")

                # 3. Perform balance updates
                debit_resp = await client.put(f"{settings.ACCOUNT_SERVICE_URL}/accounts/internal/{from_account_id}/balance?delta=-{amount}")
                if debit_resp.status_code != 200:
                    raise HTTPException(status_code=500, detail="Debit failed")
                
                credit_resp = await client.put(f"{settings.ACCOUNT_SERVICE_URL}/accounts/internal/{to_account_id}/balance?delta={amount}")
                if credit_resp.status_code != 200:
                    # Rolling back debit... (in a real system we'd use sagas)
                    await client.put(f"{settings.ACCOUNT_SERVICE_URL}/accounts/internal/{from_account_id}/balance?delta={amount}")
                    raise HTTPException(status_code=500, detail="Credit failed")

                # 4. Record transaction in DB
                txn = transaction_repo.create(db, str(from_account_id), str(to_account_id), amount)

                # 5. Publish Event
                publish_event('transaction.completed', {
                    'transaction_id': str(txn.id),
                    'from_account': str(from_account_id),
                    'to_account': str(to_account_id),
                    'amount': amount,
                    'type': txn.type,
                    'timestamp': txn.created_at.isoformat()
                })

                return txn

        finally:
            release_lock(ids[0], lock1)
            release_lock(ids[1], lock2)

    def delete(self, db: Session, txn_id: str, role: str):
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        txn = transaction_repo.delete(db, txn_id)
        if not txn:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction deleted"}

transaction_service = TransactionService()

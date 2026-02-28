import redis
import uuid
from fastapi import HTTPException
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def acquire_lock(account_id: str, ttl: int = 10) -> str:
    lock_key = f'lock:account:{account_id}'
    lock_value = str(uuid.uuid4())
    acquired = redis_client.set(lock_key, lock_value, nx=True, ex=ttl)
    if not acquired:
        raise HTTPException(status_code=409, detail='Account busy, please retry')
    return lock_value

def release_lock(account_id: str, lock_value: str):
    lock_key = f'lock:account:{account_id}'
    current = redis_client.get(lock_key)
    if current and current.decode() == lock_value:
        redis_client.delete(lock_key)

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.exceptions.custom_exceptions import RateLimitExceededException
from app.api.routes.transactions import redis_client

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, limit: int = 100, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        # Basic rate limiter by ip
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Redis logic
        requests = redis_client.incr(key)
        if requests == 1:
            redis_client.expire(key, self.window)
            
        if requests > self.limit:
            raise RateLimitExceededException()
            
        return await call_next(request)

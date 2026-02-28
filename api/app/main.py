from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, accounts, transactions, loans, admin, users
from app.middleware.cors import add_cors_middleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.exceptions.exception_handlers import add_exception_handlers

app = FastAPI(title=settings.PROJECT_NAME)

add_cors_middleware(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)
add_exception_handlers(app)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(loans.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Digital Banking API"}

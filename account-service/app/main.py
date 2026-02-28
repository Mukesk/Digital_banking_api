from fastapi import FastAPI
from app.routes import accounts
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Account Service")

app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])

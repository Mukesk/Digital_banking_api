from fastapi import FastAPI
from app.routes import transactions
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transaction Service")

app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

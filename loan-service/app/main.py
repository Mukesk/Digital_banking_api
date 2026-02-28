from fastapi import FastAPI
from app.routes import loans
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Service")

app.include_router(loans.router, prefix="/loans", tags=["Loans"])

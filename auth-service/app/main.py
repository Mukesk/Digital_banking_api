from fastapi import FastAPI
from app.routes import auth
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

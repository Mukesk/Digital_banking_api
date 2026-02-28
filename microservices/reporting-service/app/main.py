from fastapi import FastAPI
from app.routes import reports
from app.events.consumer import run_consumer_in_background
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_consumer_in_background()
    yield

app = FastAPI(title="Reporting Service", lifespan=lifespan)

app.include_router(reports.router, prefix="/admin/reports", tags=["Reports"])

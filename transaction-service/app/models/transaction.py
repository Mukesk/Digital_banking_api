import uuid
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_account_id = Column(UUID(as_uuid=True), index=True)
    to_account_id = Column(UUID(as_uuid=True), index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False, default="transfer")
    created_at = Column(DateTime, default=datetime.utcnow)

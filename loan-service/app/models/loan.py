import uuid
from sqlalchemy import Column, String, Float, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.pending)
    interest_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

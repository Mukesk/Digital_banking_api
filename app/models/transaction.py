import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_account = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True) # None for deposit
    to_account = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True) # None for withdrawal
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # transfer/deposit/withdrawal
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    source_account = relationship("Account", foreign_keys=[from_account])
    destination_account = relationship("Account", foreign_keys=[to_account])

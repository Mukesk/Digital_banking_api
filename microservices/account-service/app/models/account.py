import uuid
import string
import random
from sqlalchemy import Column, String, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AccountStatus(str, enum.Enum):
    active = "active"
    frozen = "frozen"

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    account_number = Column(String, unique=True, index=True, default=generate_account_number)
    balance = Column(Float, default=0.0)
    status = Column(Enum(AccountStatus), default=AccountStatus.active)

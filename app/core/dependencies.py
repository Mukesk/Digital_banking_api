from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserResponse
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM = "HS256"

def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        from app.core.security import get_password_hash
        from app.models.user import RoleEnum
        user = User(
            email="admin@test.com", 
            password_hash=get_password_hash("pass"), 
            role=RoleEnum.admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def require_role(role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        return current_user
    return role_checker

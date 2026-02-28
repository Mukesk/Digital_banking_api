from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.models.user import User, RoleEnum
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    def register_user(self, db: Session, user_in: UserCreate):
        existing_user = user_repo.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(user_in.password)
        # Parse role safely
        try:
            role_enum = RoleEnum(user_in.role)
        except ValueError:
            role_enum = RoleEnum.customer
            
        new_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            role=role_enum
        )
        return user_repo.create(db, new_user)

    def authenticate_user(self, db: Session, email: str, password: str):
        user = user_repo.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

auth_service = AuthService()

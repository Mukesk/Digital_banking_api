from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.models.user import User, RoleEnum
from app.schemas.user_schema import UserResponse
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])

class UserProfileUpdate(BaseModel):
    email: EmailStr

@router.put("/profile", response_model=UserResponse)
def update_profile(
    profile_in: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.customer.value))
):
    # Check if email is already completely in use
    existing_user = db.query(User).filter(User.email == profile_in.email, User.id != current_user.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already taken")
        
    current_user.email = profile_in.email
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.customer.value))
):
    db.delete(current_user)
    db.commit()

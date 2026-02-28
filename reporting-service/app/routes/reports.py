from fastapi import APIRouter, Depends, HTTPException
from app.services.report_service import report_service
from app.core.security import get_current_user

router = APIRouter()

@router.get("")
def get_reports(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return report_service.get_dashboard_metrics()

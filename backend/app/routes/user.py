from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UpdateProfile, UpdateNotification

router = APIRouter()

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "notification_frequency": current_user.notification_frequency
    }

@router.put("/update-profile")

@router.put("/update-profile")
def update_profile(
    name: str = None,
    field: str = None,
    skills: str = None,
    preferred_location: str = None,
    notification_frequency: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if name: current_user.name = name
    if field: current_user.field = field
    if skills: current_user.skills = skills
    if preferred_location: current_user.preferred_location = preferred_location
    if notification_frequency: current_user.notification_frequency = notification_frequency
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated"}    


@router.put("/update-notification")
def update_notification(
    data: UpdateNotification,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.notification_frequency = data.notification_frequency
    db.commit()
    db.refresh(current_user)

    return {"message": "NotificationUupdated"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.notification import NotificationResponse
from app.services.notification_service import NotificationService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# Customer - View all own notifications
@router.get("/me", response_model=list[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.get_my_notifications(
        db,
        current_user.id
    )


# Customer - View unread notifications
@router.get("/me/unread", response_model=list[NotificationResponse])
def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.get_unread_notifications(
        db,
        current_user.id
    )


# Customer - Mark notification as read
@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.mark_as_read(
        db,
        notification_id,
        current_user.id
    )
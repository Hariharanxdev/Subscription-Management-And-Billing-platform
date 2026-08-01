from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationService:

    # Create notification
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str
    ):
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False
        )

        return NotificationRepository.create_notification(
            db,
            notification
        )

    # Customer - Get all own notifications
    @staticmethod
    def get_my_notifications(
        db: Session,
        user_id: int
    ):
        return NotificationRepository.get_user_notifications(
            db,
            user_id
        )

    # Customer - Get unread notifications
    @staticmethod
    def get_unread_notifications(
        db: Session,
        user_id: int
    ):
        return NotificationRepository.get_unread_notifications(
            db,
            user_id
        )

    # Customer - Mark notification as read
    @staticmethod
    def mark_as_read(
        db: Session,
        notification_id: int,
        user_id: int
    ):
        notification = NotificationRepository.get_notification_by_id(
            db,
            notification_id
        )

        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found"
            )

        # Customer can modify only their own notification
        if notification.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own notifications."
            )

        notification.is_read = True

        return NotificationRepository.update_notification(
            db,
            notification
        )
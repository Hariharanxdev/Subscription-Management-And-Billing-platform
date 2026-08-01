'''from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:

    # Create notification
    @staticmethod
    def create_notification(
        db: Session,
        notification: Notification
    ):
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    # Get all notifications for a customer
    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    # Get unread notifications
    @staticmethod
    def get_unread_notifications(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .order_by(Notification.created_at.desc())
            .all()
        )

    # Get one notification
    @staticmethod
    def get_notification_by_id(
        db: Session,
        notification_id: int
    ):
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    # Update notification
    @staticmethod
    def update_notification(
        db: Session,
        notification: Notification
    ):
        db.commit()
        db.refresh(notification)

        return notification


        @staticmethod
        def reminder_exists(
            db: Session,
            user_id: int,
            message: str
        ):
            return (
                db.query(Notification)
                .filter(
                    Notification.user_id == user_id,
                    Notification.notification_type == "expiry_reminder",
                    Notification.message == message
                )
                .first()
            )'''

from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:

    # Create notification
    @staticmethod
    def create_notification(
        db: Session,
        notification: Notification
    ):
        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    # Get all notifications for a user
    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    # Get unread notifications
    @staticmethod
    def get_unread_notifications(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .order_by(Notification.created_at.desc())
            .all()
        )

    # Get notification by ID
    @staticmethod
    def get_notification_by_id(
        db: Session,
        notification_id: int
    ):
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    # Update notification
    @staticmethod
    def update_notification(
        db: Session,
        notification: Notification
    ):
        db.commit()
        db.refresh(notification)

        return notification

    # Check whether expiry reminder already exists
    @staticmethod
    def reminder_exists(
        db: Session,
        user_id: int,
        message: str
    ):
        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.notification_type == "expiry_reminder",
                Notification.message == message
            )
            .first()
        )
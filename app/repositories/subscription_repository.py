from datetime import date

from sqlalchemy.orm import Session

from app.models.subscription import Subscription


class SubscriptionRepository:

    @staticmethod
    def create_subscription(
        db: Session,
        subscription: Subscription
    ):
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def get_subscription_by_id(
        db: Session,
        subscription_id: int
    ):
        return (
            db.query(Subscription)
            .filter(Subscription.id == subscription_id)
            .first()
        )

    @staticmethod
    def get_user_subscriptions(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_all_subscriptions(db: Session):
        return db.query(Subscription).all()

    @staticmethod
    def update_subscription(
        db: Session,
        subscription: Subscription
    ):
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def delete_subscription(
        db: Session,
        subscription: Subscription
    ):
        db.delete(subscription)
        db.commit()

    @staticmethod
    def get_active_subscription(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "active"
            )
            .first()
        )

    @staticmethod
    def get_expired_active_subscriptions(
        db: Session
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.end_date < date.today()
            )
            .all()
        )

    @staticmethod
    def get_subscriptions_expiring_on(
        db: Session,
        target_date: date
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.end_date == target_date
            )
            .all()
        )
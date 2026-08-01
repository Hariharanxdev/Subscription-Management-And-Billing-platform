from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.subscription_plan import SubscriptionPlan
from app.models.subscription import Subscription
from app.models.payment import Payment
from app.models.invoice import Invoice


class DashboardRepository:

    @staticmethod
    def get_total_users(db: Session):
        return db.query(User).count()

    @staticmethod
    def get_total_plans(db: Session):
        return db.query(SubscriptionPlan).count()

    @staticmethod
    def get_total_subscriptions(db: Session):
        return db.query(Subscription).count()

    @staticmethod
    def get_subscription_count_by_status(
        db: Session,
        status: str
    ):
        return (
            db.query(Subscription)
            .filter(Subscription.status == status)
            .count()
        )

    @staticmethod
    def get_total_payments(db: Session):
        return db.query(Payment).count()

    @staticmethod
    def get_total_revenue(db: Session):
        total = (
            db.query(func.sum(Payment.amount))
            .filter(Payment.payment_status == "success")
            .scalar()
        )

        return total or 0

    @staticmethod
    def get_total_invoices(db: Session):
        return db.query(Invoice).count()
    @staticmethod
    def get_recent_payments(
        db: Session,
        limit: int = 5
    ):
        return (
            db.query(Payment)
            .order_by(Payment.payment_date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_recent_subscriptions(
        db: Session,
        limit: int = 5
    ):
        return (
            db.query(Subscription)
            .order_by(Subscription.id.desc())
            .limit(limit)
            .all()
        )


    @staticmethod
    def get_successful_payments(db: Session):
        return (
            db.query(Payment)
            .filter(Payment.payment_status == "success")
            .all()
        )

    # CUSTOMER DASHBOARD

    @staticmethod
    def get_customer_active_subscription(
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
    def get_customer_successful_payments(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Payment)
            .join(
                Subscription,
                Payment.subscription_id == Subscription.id
            )
            .filter(
                Subscription.user_id == user_id,
                Payment.payment_status == "success"
            )
            .all()
        )

    @staticmethod
    def get_customer_invoice_count(
        db: Session,
        user_id: int
    ):
        return (
            db.query(Invoice)
            .join(
                Payment,
                Invoice.payment_id == Payment.id
            )
            .join(
                Subscription,
                Payment.subscription_id == Subscription.id
            )
            .filter(
                Subscription.user_id == user_id
            )
            .count()
        )
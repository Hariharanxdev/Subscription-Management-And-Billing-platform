from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def create_payment(db: Session, payment: Payment):
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int):
        return (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    @staticmethod
    def get_all_payments(db: Session):
        return db.query(Payment).all()

    @staticmethod
    def get_payments_by_subscription(db: Session, subscription_id: int):
        return (
            db.query(Payment)
            .filter(Payment.subscription_id == subscription_id)
            .all()
        )
    @staticmethod
    def get_successful_payment_by_subscription(
        db: Session,
        subscription_id: int
    ):
        return (
            db.query(Payment)
            .filter(
                Payment.subscription_id == subscription_id,
                Payment.payment_status == "success"
            )
            .first()
        )

    @staticmethod
    def update_payment(db: Session, payment: Payment):
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def delete_payment(db: Session, payment: Payment):
        db.delete(payment)
        db.commit()
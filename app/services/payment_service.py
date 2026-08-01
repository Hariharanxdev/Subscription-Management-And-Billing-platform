import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.subscription_plan_repository import SubscriptionPlanRepository
from app.services.invoice_service import InvoiceService
from app.services.notification_service import NotificationService


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        user_id: int,
        subscription_id: int,
        payment_method: str
    ):
        # Find subscription
        subscription = SubscriptionRepository.get_subscription_by_id(
            db,
            subscription_id
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # Customer can pay only for their own subscription
        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot pay for another user's subscription."
            )

        # Check whether payment was already completed
        existing_payment = (
            PaymentRepository.get_successful_payment_by_subscription(
                db,
                subscription_id
            )
        )

        if existing_payment:
            raise HTTPException(
                status_code=400,
                detail="Payment has already been completed for this subscription."
            )

        # Find subscription plan
        plan = SubscriptionPlanRepository.get_by_id(
            db,
            subscription.plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        # Generate unique transaction ID
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

        # Create payment
        payment = Payment(
            subscription_id=subscription.id,
            amount=plan.price,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_status="success"
        )

        payment = PaymentRepository.create_payment(
            db,
            payment
        )

        # Automatically generate invoice after successful payment
        InvoiceService.create_invoice(
            db,
            payment.id
        )

        # Automatically create payment success notification
        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title="Payment Successful",
            message=(
                f"Your payment of ₹{payment.amount:.2f} "
                f"for {plan.plan_name} was completed successfully."
            ),
            notification_type="payment_success"
        )

        return payment

    @staticmethod
    def get_payment(
        db: Session,
        payment_id: int,
        user_id: int
    ):
        payment = PaymentRepository.get_payment_by_id(
            db,
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        subscription = SubscriptionRepository.get_subscription_by_id(
            db,
            payment.subscription_id
        )

        # Customer can view only their own payment
        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own payments."
            )

        return payment

    @staticmethod
    def get_all_payments(db: Session):
        return PaymentRepository.get_all_payments(db)

    @staticmethod
    def get_subscription_payments(
        db: Session,
        subscription_id: int,
        user_id: int
    ):
        subscription = SubscriptionRepository.get_subscription_by_id(
            db,
            subscription_id
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # Customer can view only their own subscription payments
        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view payments for your own subscription."
            )

        return PaymentRepository.get_payments_by_subscription(
            db,
            subscription_id
        )
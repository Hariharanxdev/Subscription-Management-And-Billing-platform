import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment

from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.subscription_plan_repository import (
    SubscriptionPlanRepository
)
from app.repositories.user_repository import UserRepository

from app.services.invoice_service import InvoiceService
from app.services.notification_service import NotificationService
from app.services.email_service import EmailService


class PaymentService:

    # ============================================================
    # CREATE PAYMENT
    # ============================================================

    @staticmethod
    def create_payment(
        db: Session,
        user_id: int,
        subscription_id: int,
        payment_method: str,
        payment_status: str = "success"
    ):

        # --------------------------------------------------------
        # 1. Find subscription
        # --------------------------------------------------------

        subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                subscription_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # --------------------------------------------------------
        # 2. Check ownership
        # --------------------------------------------------------

        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You cannot pay for another user's subscription."
                )
            )

        # --------------------------------------------------------
        # 3. Validate payment status
        # --------------------------------------------------------

        payment_status = payment_status.lower().strip()

        if payment_status not in ["success", "failed"]:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid payment status. "
                    "Use 'success' or 'failed'."
                )
            )

        # --------------------------------------------------------
        # 4. Check duplicate successful payment
        # --------------------------------------------------------

        existing_payment = (
            PaymentRepository.get_successful_payment_by_subscription(
                db,
                subscription_id
            )
        )

        if existing_payment:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Payment has already been completed "
                    "for this subscription."
                )
            )

        # --------------------------------------------------------
        # 5. Find subscription plan
        # --------------------------------------------------------

        plan = SubscriptionPlanRepository.get_by_id(
            db,
            subscription.plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        # --------------------------------------------------------
        # 6. Generate transaction ID
        # --------------------------------------------------------

        transaction_id = (
            f"TXN-{uuid.uuid4().hex[:12].upper()}"
        )

        # --------------------------------------------------------
        # 7. Create payment
        # --------------------------------------------------------

        payment = Payment(
            subscription_id=subscription.id,
            amount=plan.price,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_status=payment_status
        )

        # --------------------------------------------------------
        # 8. Save payment
        # --------------------------------------------------------

        payment = PaymentRepository.create_payment(
            db,
            payment
        )

        print(
            f"[PAYMENT] Payment created: "
            f"id={payment.id}, "
            f"transaction_id={payment.transaction_id}, "
            f"status={payment.payment_status}, "
            f"amount={payment.amount}"
        )

        # --------------------------------------------------------
        # 9. Get customer
        # --------------------------------------------------------

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            print(
                f"[PAYMENT] User not found: user_id={user_id}"
            )

        # ========================================================
        # SUCCESS PAYMENT
        # ========================================================

        if payment_status == "success":

            # ----------------------------------------------------
            # Create invoice ONLY for successful payment
            # ----------------------------------------------------

            InvoiceService.create_invoice(
                db,
                payment.id
            )

            print(
                f"[PAYMENT] Invoice created "
                f"for payment_id={payment.id}"
            )

            # ----------------------------------------------------
            # Create success notification
            # ----------------------------------------------------

            NotificationService.create_notification(
                db=db,
                user_id=user_id,
                title="Payment Successful",
                message=(
                    f"Your payment of ₹{payment.amount:.2f} "
                    f"for {plan.plan_name} "
                    f"was completed successfully."
                ),
                notification_type="payment_success"
            )

            print(
                f"[PAYMENT] Success notification created "
                f"for user_id={user_id}"
            )

            # ----------------------------------------------------
            # Send success email
            # ----------------------------------------------------

            if user and user.email:

                print(
                    f"[PAYMENT EMAIL] "
                    f"Sending success email to {user.email}"
                )

                try:

                    email_sent = (
                        EmailService.send_payment_success_email(
                            to_email=user.email,
                            username=user.username,
                            amount=payment.amount,
                            plan_name=plan.plan_name,
                            transaction_id=payment.transaction_id,
                            payment_method=payment.payment_method
                        )
                    )

                    print(
                        f"[PAYMENT EMAIL] "
                        f"Success email result: {email_sent}"
                    )

                except Exception as email_error:

                    print(
                        f"[PAYMENT EMAIL ERROR] "
                        f"{email_error}"
                    )

            else:

                print(
                    "[PAYMENT EMAIL] "
                    "No customer email found."
                )

        # ========================================================
        # FAILED PAYMENT
        # ========================================================

        elif payment_status == "failed":

            # ----------------------------------------------------
            # DO NOT CREATE INVOICE
            # ----------------------------------------------------

            print(
                "[PAYMENT] Failed payment - "
                "invoice will not be created."
            )

            # ----------------------------------------------------
            # Create failed notification
            # ----------------------------------------------------

            NotificationService.create_notification(
                db=db,
                user_id=user_id,
                title="Payment Failed",
                message=(
                    f"Your payment of ₹{payment.amount:.2f} "
                    f"for {plan.plan_name} failed. "
                    f"Please try again."
                ),
                notification_type="payment_failed"
            )

            print(
                f"[PAYMENT] Failed notification created "
                f"for user_id={user_id}"
            )

            # ----------------------------------------------------
            # Send failed payment email
            # ----------------------------------------------------

            if user and user.email:

                print(
                    f"[PAYMENT EMAIL] "
                    f"Sending failed-payment email "
                    f"to {user.email}"
                )

                try:

                    email_sent = (
                        EmailService.send_payment_failed_email(
                            to_email=user.email,
                            username=user.username,
                            amount=payment.amount,
                            plan_name=plan.plan_name,
                            transaction_id=payment.transaction_id,
                            payment_method=payment.payment_method
                        )
                    )

                    print(
                        f"[PAYMENT EMAIL] "
                        f"Failed-payment email result: "
                        f"{email_sent}"
                    )

                except Exception as email_error:

                    print(
                        f"[PAYMENT EMAIL ERROR] "
                        f"{email_error}"
                    )

            else:

                print(
                    "[PAYMENT EMAIL] "
                    "No customer email found."
                )

        # --------------------------------------------------------
        # Return payment
        # --------------------------------------------------------

        return payment

    # ============================================================
    # GET ONE PAYMENT
    # ============================================================

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

        subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                payment.subscription_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own payments."
            )

        return payment

    # ============================================================
    # GET ALL PAYMENTS
    # ============================================================

    @staticmethod
    def get_all_payments(
        db: Session
    ):

        return PaymentRepository.get_all_payments(
            db
        )

    # ============================================================
    # GET SUBSCRIPTION PAYMENTS
    # ============================================================

    @staticmethod
    def get_subscription_payments(
        db: Session,
        subscription_id: int,
        user_id: int
    ):

        subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                subscription_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You can only view payments "
                    "for your own subscription."
                )
            )

        return PaymentRepository.get_payments_by_subscription(
            db,
            subscription_id
        )
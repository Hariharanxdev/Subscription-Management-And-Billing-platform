import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository

from app.services.email_service import EmailService


class InvoiceService:

    # ============================================================
    # CREATE INVOICE
    # ============================================================

    @staticmethod
    def create_invoice(
        db: Session,
        payment_id: int
    ):

        # --------------------------------------------------------
        # 1. Find payment
        # --------------------------------------------------------

        payment = PaymentRepository.get_payment_by_id(
            db,
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        # --------------------------------------------------------
        # 2. Invoice only for successful payment
        # --------------------------------------------------------

        if payment.payment_status != "success":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invoice can only be generated "
                    "for successful payments."
                )
            )

        # --------------------------------------------------------
        # 3. Prevent duplicate invoice
        # --------------------------------------------------------

        existing_invoice = (
            InvoiceRepository.get_invoice_by_payment_id(
                db,
                payment_id
            )
        )

        if existing_invoice:
            return existing_invoice

        # --------------------------------------------------------
        # 4. Generate invoice number
        # --------------------------------------------------------

        invoice_number = (
            f"INV-{uuid.uuid4().hex[:10].upper()}"
        )

        # --------------------------------------------------------
        # 5. Create invoice
        # --------------------------------------------------------

        invoice = Invoice(
            payment_id=payment.id,
            invoice_number=invoice_number,
            amount=payment.amount,
            status="paid"
        )

        # --------------------------------------------------------
        # 6. Save invoice
        # --------------------------------------------------------

        invoice = InvoiceRepository.create_invoice(
            db,
            invoice
        )

        print(
            f"[INVOICE] Invoice created successfully: "
            f"{invoice.invoice_number}"
        )

        # --------------------------------------------------------
        # 7. Find subscription
        # --------------------------------------------------------

        subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                payment.subscription_id
            )
        )

        if not subscription:
            print(
                "[INVOICE EMAIL] Subscription not found. "
                "Invoice email skipped."
            )

            return invoice

        # --------------------------------------------------------
        # 8. Find customer
        # --------------------------------------------------------

        user = UserRepository.get_by_id(
            db,
            subscription.user_id
        )

        if not user:
            print(
                "[INVOICE EMAIL] Customer not found. "
                "Invoice email skipped."
            )

            return invoice

        # --------------------------------------------------------
        # 9. Send invoice email
        # --------------------------------------------------------

        if not user.email:

            print(
                "[INVOICE EMAIL] Customer has no email address."
            )

            return invoice

        print(
            f"[INVOICE EMAIL] "
            f"Sending invoice email to {user.email}"
        )

        try:

            email_sent = (
                EmailService.send_invoice_generated_email(
                    to_email=user.email,
                    username=user.username,
                    invoice_number=invoice.invoice_number,
                    amount=invoice.amount,
                    transaction_id=payment.transaction_id,
                    payment_method=payment.payment_method,
                    status=invoice.status
                )
            )

            print(
                f"[INVOICE EMAIL] "
                f"Email result: {email_sent}"
            )

            if email_sent:

                print(
                    f"[INVOICE EMAIL SUCCESS] "
                    f"Invoice email sent to {user.email}"
                )

            else:

                print(
                    f"[INVOICE EMAIL ERROR] "
                    f"Invoice email failed for {user.email}"
                )

        except Exception as email_error:

            print(
                f"[INVOICE EMAIL ERROR] "
                f"{email_error}"
            )

        # --------------------------------------------------------
        # 10. Return invoice
        # --------------------------------------------------------

        return invoice

    # ============================================================
    # GET ONE INVOICE
    # ============================================================

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_id: int,
        user_id: int,
        user_role: str
    ):

        invoice = InvoiceRepository.get_invoice_by_id(
            db,
            invoice_id
        )

        if not invoice:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        payment = PaymentRepository.get_payment_by_id(
            db,
            invoice.payment_id
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

        # Admin can view any invoice.
        # Customer can view only their own invoice.
        if (
            user_role != "admin"
            and subscription.user_id != user_id
        ):
            raise HTTPException(
                status_code=403,
                detail="You can only view your own invoices."
            )

        return invoice

    # ============================================================
    # GET MY INVOICES
    # ============================================================

    @staticmethod
    def get_my_invoices(
        db: Session,
        user_id: int
    ):

        invoices = InvoiceRepository.get_all_invoices(
            db
        )

        my_invoices = []

        for invoice in invoices:

            payment = PaymentRepository.get_payment_by_id(
                db,
                invoice.payment_id
            )

            if not payment:
                continue

            subscription = (
                SubscriptionRepository.get_subscription_by_id(
                    db,
                    payment.subscription_id
                )
            )

            if not subscription:
                continue

            if subscription.user_id == user_id:
                my_invoices.append(invoice)

        return my_invoices

    # ============================================================
    # GET ALL INVOICES
    # ============================================================

    @staticmethod
    def get_all_invoices(
        db: Session
    ):

        return InvoiceRepository.get_all_invoices(
            db
        )
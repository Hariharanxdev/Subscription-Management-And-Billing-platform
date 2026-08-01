import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.subscription_repository import SubscriptionRepository


class InvoiceService:

    @staticmethod
    def create_invoice(db: Session, payment_id: int):
        # Find payment
        payment = PaymentRepository.get_payment_by_id(
            db,
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        # Invoice should be created only for successful payment
        if payment.payment_status != "success":
            raise HTTPException(
                status_code=400,
                detail="Invoice can only be generated for successful payments."
            )

        # Prevent duplicate invoice
        existing_invoice = InvoiceRepository.get_invoice_by_payment_id(
            db,
            payment_id
        )

        if existing_invoice:
            return existing_invoice

        # Generate unique invoice number
        invoice_number = f"INV-{uuid.uuid4().hex[:10].upper()}"

        invoice = Invoice(
            payment_id=payment.id,
            invoice_number=invoice_number,
            amount=payment.amount,
            status="paid"
        )

        return InvoiceRepository.create_invoice(
            db,
            invoice
        )

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

        subscription = SubscriptionRepository.get_subscription_by_id(
            db,
            payment.subscription_id
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # Admin can view any invoice.
        # Customer can view only their own invoice.
        if user_role != "admin" and subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own invoices."
            )

        return invoice

    @staticmethod
    def get_my_invoices(
        db: Session,
        user_id: int
    ):
        invoices = InvoiceRepository.get_all_invoices(db)

        my_invoices = []

        for invoice in invoices:
            payment = PaymentRepository.get_payment_by_id(
                db,
                invoice.payment_id
            )

            subscription = SubscriptionRepository.get_subscription_by_id(
                db,
                payment.subscription_id
            )

            if subscription.user_id == user_id:
                my_invoices.append(invoice)

        return my_invoices

    @staticmethod
    def get_all_invoices(db: Session):
        return InvoiceRepository.get_all_invoices(db)
from sqlalchemy.orm import Session

from app.models.invoice import Invoice


class InvoiceRepository:

    @staticmethod
    def create_invoice(db: Session, invoice: Invoice):
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def get_invoice_by_id(db: Session, invoice_id: int):
        return (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

    @staticmethod
    def get_invoice_by_payment_id(db: Session, payment_id: int):
        return (
            db.query(Invoice)
            .filter(Invoice.payment_id == payment_id)
            .first()
        )

    @staticmethod
    def get_all_invoices(db: Session):
        return db.query(Invoice).all()
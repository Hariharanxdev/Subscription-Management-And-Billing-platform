from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.invoice import InvoiceResponse
from app.services.invoice_service import InvoiceService
from app.services.invoice_pdf_service import InvoicePDFService
from app.core.security import get_current_user
from app.core.dependencies import get_current_admin
from app.models.user import User


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


# Customer - View own invoices
@router.get("/me", response_model=list[InvoiceResponse])
def get_my_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InvoiceService.get_my_invoices(
        db,
        current_user.id
    )


# Admin - View all invoices
@router.get("/", response_model=list[InvoiceResponse])
def get_all_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return InvoiceService.get_all_invoices(db)


# Customer - View one own invoice
@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return InvoiceService.get_invoice(
        db,
        invoice_id,
        current_user.id,
        current_user.role
    )

@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get invoice + perform ownership/admin security check
    invoice = InvoiceService.get_invoice(
        db,
        invoice_id,
        current_user.id,
        current_user.role
    )

    payment = invoice.payment
    subscription = payment.subscription
    plan = subscription.plan
    user = subscription.user

    pdf_buffer = InvoicePDFService.generate_invoice_pdf(
        invoice=invoice,
        payment=payment,
        subscription=subscription,
        plan=plan,
        user=user
    )

    filename = f"{invoice.invoice_number}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
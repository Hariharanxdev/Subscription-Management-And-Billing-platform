from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService
from app.core.security import get_current_user
from app.core.dependencies import get_current_admin
from app.models.user import User


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# Customer - Make payment
@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.create_payment(
        db,
        current_user.id,
        payment.subscription_id,
        payment.payment_method
    )


# Admin - View all payments
@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return PaymentService.get_all_payments(db)


# Customer/Admin - Get one payment
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_payment(
        db,
        payment_id,
        current_user.id
    )


# View payments for a subscription
@router.get(
    "/subscription/{subscription_id}",
    response_model=list[PaymentResponse]
)
def get_subscription_payments(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_subscription_payments(
        db,
        subscription_id,
        current_user.id
    )
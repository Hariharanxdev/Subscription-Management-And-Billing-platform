from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentCreate(BaseModel):
    subscription_id: int
    payment_method: str
    payment_status: str = "success"


class PaymentResponse(BaseModel):
    id: int
    subscription_id: int
    amount: float
    payment_method: str
    transaction_id: str
    payment_status: str
    payment_date: datetime

    class Config:
        from_attributes = True


class PaymentUpdate(BaseModel):
    payment_status: Optional[str] = None
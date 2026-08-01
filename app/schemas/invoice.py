from datetime import datetime
from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    id: int
    payment_id: int
    invoice_number: str
    amount: float
    status: str
    issued_at: datetime

    class Config:
        from_attributes = True
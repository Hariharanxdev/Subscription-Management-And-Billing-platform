from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(
        Integer,
        ForeignKey("payments.id"),
        nullable=False,
        unique=True
    )

    invoice_number = Column(
        String,
        unique=True,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(20),
        default="paid"
    )

    issued_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationship
    payment = relationship(
        "Payment",
        back_populates="invoice"
    )
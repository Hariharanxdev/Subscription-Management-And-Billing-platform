from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    transaction_id = Column(
        String,
        unique=True,
        nullable=False
    )

    payment_status = Column(
        String,
        default="pending"
    )

    payment_date = Column(
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

    # Relationship with Subscription
    subscription = relationship(
        "Subscription",
        back_populates="payments"
    )

    # One Payment -> One Invoice
    invoice = relationship(
        "Invoice",
        back_populates="payment",
        uselist=False,
        cascade="all, delete-orphan"
    )
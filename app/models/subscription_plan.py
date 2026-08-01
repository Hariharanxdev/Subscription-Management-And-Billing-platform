from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.sql import func

from app.database.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)

    plan_name = Column(String(100), unique=True, nullable=False)

    description = Column(String(255))

    price = Column(Numeric(10, 2), nullable=False)

    billing_cycle = Column(String(20), nullable=False)

    duration_days = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class SubscriptionPlanBase(BaseModel):
    plan_name: str
    description: str
    price: Decimal
    billing_cycle: str
    duration_days: int


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(SubscriptionPlanBase):
    pass


class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
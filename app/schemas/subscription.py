from datetime import date
from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan_id: int


# Plan information shown inside subscription
class PlanInfo(BaseModel):
    id: int
    plan_name: str
    price: float

    class Config:
        from_attributes = True


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: date
    end_date: date
    status: str

    # Include plan details
    plan: PlanInfo

    class Config:
        from_attributes = True
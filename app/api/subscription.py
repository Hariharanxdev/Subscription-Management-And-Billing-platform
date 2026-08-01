from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse
)
from app.services.subscription_service import SubscriptionService
from app.core.security import get_current_user
from app.core.dependencies import get_current_admin
from app.models.user import User


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# Customer - Subscribe to a plan
@router.post("/", response_model=SubscriptionResponse)
def subscribe(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SubscriptionService.subscribe(
        db,
        current_user.id,
        subscription.plan_id
    )


# Customer - View own subscriptions
@router.get("/me", response_model=list[SubscriptionResponse])
def get_my_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SubscriptionService.get_my_subscriptions(
        db,
        current_user.id
    )


# Admin - View all subscriptions
@router.get("/", response_model=list[SubscriptionResponse])
def get_all_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return SubscriptionService.get_all_subscriptions(db)


# Admin - Check and update expired subscriptions
@router.post("/check-expired")
def check_expired_subscriptions(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return SubscriptionService.update_expired_subscriptions(db)
# Customer - Renew expired subscription
@router.post(
    "/{subscription_id}/renew",
    response_model=SubscriptionResponse
)
def renew_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SubscriptionService.renew_subscription(
        db,
        subscription_id,
        current_user.id
    )


# Customer - Cancel own subscription
@router.put(
    "/{subscription_id}/cancel",
    response_model=SubscriptionResponse
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return SubscriptionService.cancel_subscription(
        db,
        subscription_id,
        current_user.id
    )
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.subscription_plan import (
    SubscriptionPlanCreate,
    SubscriptionPlanResponse
)
from app.services.subscription_plan_service import SubscriptionPlanService

router = APIRouter(prefix="/plans", tags=["Subscription Plans"])


@router.post("/", response_model=SubscriptionPlanResponse)
def create_plan(
    plan: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return SubscriptionPlanService.create_plan(db, plan)


@router.get("/", response_model=list[SubscriptionPlanResponse])
def get_plans(db: Session = Depends(get_db)):
    return SubscriptionPlanService.get_all_plans(db)


@router.get("/{plan_id}", response_model=SubscriptionPlanResponse)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    plan = SubscriptionPlanService.get_plan(db, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return plan
@router.put("/{plan_id}", response_model=SubscriptionPlanResponse)
def update_plan(
    plan_id: int,
    plan_data: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    plan = SubscriptionPlanService.get_plan(db, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return SubscriptionPlanService.update_plan(db, plan, plan_data)
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    plan = SubscriptionPlanService.get_plan(db, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    SubscriptionPlanService.delete_plan(db, plan)

    return {
        "message": "Subscription plan deleted successfully"
    }
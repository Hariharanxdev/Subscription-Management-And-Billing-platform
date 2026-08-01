from sqlalchemy.orm import Session

from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription_plan import SubscriptionPlanCreate


class SubscriptionPlanRepository:

    @staticmethod
    def create(db: Session, plan: SubscriptionPlanCreate):

        new_plan = SubscriptionPlan(
            plan_name=plan.plan_name,
            description=plan.description,
            price=plan.price,
            billing_cycle=plan.billing_cycle,
            duration_days=plan.duration_days
        )

        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        return new_plan

    @staticmethod
    def get_all(db: Session):
        return db.query(SubscriptionPlan).all()

    @staticmethod
    def get_by_id(db: Session, plan_id: int):
        return db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id
        ).first()

    @staticmethod
    def delete(db: Session, plan):
        db.delete(plan)
        db.commit()

    @staticmethod
    def update(db: Session, plan: SubscriptionPlan, plan_data):

        plan.plan_name = plan_data.plan_name
        plan.description = plan_data.description
        plan.price = plan_data.price
        plan.billing_cycle = plan_data.billing_cycle
        plan.duration_days = plan_data.duration_days

        db.commit()
        db.refresh(plan)

        return plan
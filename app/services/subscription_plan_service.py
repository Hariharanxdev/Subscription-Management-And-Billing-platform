from sqlalchemy.orm import Session

from app.repositories.subscription_plan_repository import SubscriptionPlanRepository
from app.schemas.subscription_plan import SubscriptionPlanCreate


class SubscriptionPlanService:

    @staticmethod
    def create_plan(db: Session, plan: SubscriptionPlanCreate):
        return SubscriptionPlanRepository.create(db, plan)

    @staticmethod
    def get_all_plans(db: Session):
        return SubscriptionPlanRepository.get_all(db)

    @staticmethod
    def get_plan(db: Session, plan_id: int):
        return SubscriptionPlanRepository.get_by_id(db, plan_id)

    @staticmethod
    def delete_plan(db: Session, plan):
        SubscriptionPlanRepository.delete(db, plan)

    @staticmethod
    def update_plan(db: Session, plan, plan_data):
        return SubscriptionPlanRepository.update(db, plan, plan_data)
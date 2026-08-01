from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.subscription_plan_repository import (
    SubscriptionPlanRepository
)

from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService


class SubscriptionService:

   
    # CREATE NEW SUBSCRIPTION
    
    @staticmethod
    def subscribe(
        db: Session,
        user_id: int,
        plan_id: int
    ):
        # Check whether user already has an active subscription
        existing = SubscriptionRepository.get_active_subscription(
            db,
            user_id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="You already have an active subscription."
            )

        # Check whether subscription plan exists
        plan = SubscriptionPlanRepository.get_by_id(
            db,
            plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        # Calculate subscription period
        start_date = date.today()

        end_date = start_date + timedelta(
            days=plan.duration_days
        )

        subscription = Subscription(
            user_id=user_id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            status="active"
        )

        return SubscriptionRepository.create_subscription(
            db,
            subscription
        )

   
    # GET CURRENT USER SUBSCRIPTIONS
   
    @staticmethod
    def get_my_subscriptions(
        db: Session,
        user_id: int
    ):
        return SubscriptionRepository.get_user_subscriptions(
            db,
            user_id
        )

  
    # ADMIN - GET ALL SUBSCRIPTIONS
  
    @staticmethod
    def get_all_subscriptions(db: Session):
        return SubscriptionRepository.get_all_subscriptions(db)

 
    # CANCEL SUBSCRIPTION
    
    @staticmethod
    def cancel_subscription(
        db: Session,
        subscription_id: int,
        user_id: int
    ):
        subscription = SubscriptionRepository.get_subscription_by_id(
            db,
            subscription_id
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # Customer can cancel only their own subscription
        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only cancel your own subscription."
            )

        # Prevent cancelling an already cancelled subscription
        if subscription.status == "cancelled":
            raise HTTPException(
                status_code=400,
                detail="Subscription is already cancelled."
            )

        # Prevent cancelling an expired subscription
        if subscription.status == "expired":
            raise HTTPException(
                status_code=400,
                detail="Expired subscription cannot be cancelled."
            )

        subscription.status = "cancelled"

        updated_subscription = (
            SubscriptionRepository.update_subscription(
                db,
                subscription
            )
        )

        # Automatically create cancellation notification
        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title="Subscription Cancelled",
            message="Your subscription has been cancelled successfully.",
            notification_type="subscription_cancelled"
        )

        return updated_subscription

   
    # UPDATE EXPIRED SUBSCRIPTIONS
   
    @staticmethod
    def update_expired_subscriptions(db: Session):
        expired_subscriptions = (
            SubscriptionRepository.get_expired_active_subscriptions(
                db
            )
        )

        updated_count = 0

        for subscription in expired_subscriptions:

            subscription.status = "expired"

            SubscriptionRepository.update_subscription(
                db,
                subscription
            )

            # Automatically create expiry notification
            NotificationService.create_notification(
                db=db,
                user_id=subscription.user_id,
                title="Subscription Expired",
                message=(
                    "Your subscription has expired. "
                    "You can renew your subscription to continue the service."
                ),
                notification_type="subscription_expired"
            )

            updated_count += 1

        return {
            "message": "Expired subscriptions updated successfully.",
            "updated_count": updated_count
        }


    # RENEW EXPIRED SUBSCRIPTION
    
    @staticmethod
    def renew_subscription(
        db: Session,
        subscription_id: int,
        user_id: int
    ):
        # Find old subscription
        old_subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                subscription_id
            )
        )

        if not old_subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        # Customer can renew only their own subscription
        if old_subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only renew your own subscription."
            )

        # Only expired subscriptions can be renewed
        if old_subscription.status != "expired":
            raise HTTPException(
                status_code=400,
                detail="Only expired subscriptions can be renewed."
            )

        # Get plan from old subscription
        plan = SubscriptionPlanRepository.get_by_id(
            db,
            old_subscription.plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        # Prevent multiple active subscriptions
        active_subscription = (
            SubscriptionRepository.get_active_subscription(
                db,
                user_id
            )
        )

        if active_subscription:
            raise HTTPException(
                status_code=400,
                detail="You already have an active subscription."
            )

        # Create new subscription period
        start_date = date.today()

        end_date = start_date + timedelta(
            days=plan.duration_days
        )

        new_subscription = Subscription(
            user_id=user_id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            status="active"
        )

        created_subscription = (
            SubscriptionRepository.create_subscription(
                db,
                new_subscription
            )
        )

        # Automatically create renewal notification
        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title="Subscription Renewed",
            message=(
                f"Your {plan.plan_name} subscription "
                f"has been renewed successfully."
            ),
            notification_type="subscription_renewed"
        )

        return created_subscription


    
    # SEND 3-DAY EXPIRY REMINDERS
    @staticmethod
    def send_expiry_reminders(db: Session):

        target_date = date.today() + timedelta(days=3)

        subscriptions = (
            SubscriptionRepository.get_subscriptions_expiring_on(
                db,
                target_date
            )
        )

        reminder_count = 0

        for subscription in subscriptions:

            plan = SubscriptionPlanRepository.get_by_id(
                db,
                subscription.plan_id
            )

            plan_name = (
                plan.plan_name.strip()
                if plan
                else "subscription"
            )

            message = (
                f"Your {plan_name} subscription will expire "
                f"on {subscription.end_date}. "
                f"Please renew to continue your service."
            )

            # Prevent duplicate reminder
            existing_reminder = (
                NotificationRepository.reminder_exists(
                    db,
                    subscription.user_id,
                    message
                )
            )

            if existing_reminder:
                continue

            NotificationService.create_notification(
                db=db,
                user_id=subscription.user_id,
                title="Subscription Expiry Reminder",
                message=message,
                notification_type="expiry_reminder"
            )

            reminder_count += 1

        return {
            "message": "Expiry reminders processed successfully.",
            "reminder_count": reminder_count
        }
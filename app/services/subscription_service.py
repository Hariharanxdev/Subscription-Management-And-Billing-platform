from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.subscription import Subscription

from app.repositories.subscription_repository import (
    SubscriptionRepository
)

from app.repositories.subscription_plan_repository import (
    SubscriptionPlanRepository
)

from app.repositories.notification_repository import (
    NotificationRepository
)

from app.repositories.user_repository import (
    UserRepository
)

from app.services.notification_service import (
    NotificationService
)

from app.services.email_service import (
    EmailService
)


class SubscriptionService:

    # ============================================================
    # CREATE NEW SUBSCRIPTION
    # ============================================================

    @staticmethod
    def subscribe(
        db: Session,
        user_id: int,
        plan_id: int
    ):

        existing = (
            SubscriptionRepository.get_active_subscription(
                db,
                user_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail=(
                    "You already have an active subscription."
                )
            )

        plan = SubscriptionPlanRepository.get_by_id(
            db,
            plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        start_date = date.today()

        end_date = (
            start_date
            + timedelta(days=plan.duration_days)
        )

        subscription = Subscription(
            user_id=user_id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            status="active"
        )

        created_subscription = (
            SubscriptionRepository.create_subscription(
                db,
                subscription
            )
        )

        print(
            f"[SUBSCRIPTION] Created successfully: "
            f"id={created_subscription.id}, "
            f"user_id={user_id}, "
            f"plan={plan.plan_name}"
        )

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title="Subscription Activated",
            message=(
                f"Your {plan.plan_name} subscription "
                f"has been activated successfully."
            ),
            notification_type="subscription_activated"
        )

        print(
            f"[SUBSCRIPTION] Activation notification "
            f"created for user_id={user_id}"
        )

        if user and user.email:

            print(
                f"[SUBSCRIPTION EMAIL] "
                f"Sending activation email to {user.email}"
            )

            try:

                email_sent = (
                    EmailService.send_subscription_activated_email(
                        to_email=user.email,
                        username=user.username,
                        plan_name=plan.plan_name,
                        amount=plan.price,
                        start_date=created_subscription.start_date,
                        end_date=created_subscription.end_date
                    )
                )

                print(
                    f"[SUBSCRIPTION EMAIL] "
                    f"Activation email result: {email_sent}"
                )

                if email_sent:

                    print(
                        f"[SUBSCRIPTION EMAIL SUCCESS] "
                        f"Activation email sent to {user.email}"
                    )

                else:

                    print(
                        f"[SUBSCRIPTION EMAIL ERROR] "
                        f"Activation email failed for "
                        f"{user.email}"
                    )

            except Exception as email_error:

                print(
                    f"[SUBSCRIPTION EMAIL ERROR] "
                    f"{email_error}"
                )

        else:

            print(
                "[SUBSCRIPTION EMAIL] "
                "No customer email found."
            )

        return created_subscription

    # ============================================================
    # GET CURRENT USER SUBSCRIPTIONS
    # ============================================================

    @staticmethod
    def get_my_subscriptions(
        db: Session,
        user_id: int
    ):

        return SubscriptionRepository.get_user_subscriptions(
            db,
            user_id
        )

    # ============================================================
    # ADMIN - GET ALL SUBSCRIPTIONS
    # ============================================================

    @staticmethod
    def get_all_subscriptions(
        db: Session
    ):

        return SubscriptionRepository.get_all_subscriptions(
            db
        )

    # ============================================================
    # CANCEL SUBSCRIPTION
    # ============================================================

    @staticmethod
    def cancel_subscription(
        db: Session,
        subscription_id: int,
        user_id: int
    ):

        subscription = (
            SubscriptionRepository.get_subscription_by_id(
                db,
                subscription_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        if subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You can only cancel your own subscription."
                )
            )

        if subscription.status == "cancelled":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Subscription is already cancelled."
                )
            )

        if subscription.status == "expired":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Expired subscription cannot be cancelled."
                )
            )

        plan = SubscriptionPlanRepository.get_by_id(
            db,
            subscription.plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        subscription.status = "cancelled"

        updated_subscription = (
            SubscriptionRepository.update_subscription(
                db,
                subscription
            )
        )

        print(
            f"[SUBSCRIPTION] "
            f"Subscription {subscription.id} cancelled "
            f"for user_id={user_id}"
        )

        NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title="Subscription Cancelled",
            message=(
                f"Your {plan.plan_name} subscription "
                f"has been cancelled successfully."
            ),
            notification_type="subscription_cancelled"
        )

        print(
            f"[SUBSCRIPTION] "
            f"Cancellation notification created "
            f"for user_id={user_id}"
        )

        if user and user.email:

            print(
                f"[CANCELLATION EMAIL] "
                f"Sending cancellation email to {user.email}"
            )

            try:

                email_sent = (
                    EmailService
                    .send_subscription_cancelled_email(
                        to_email=user.email,
                        username=user.username,
                        plan_name=plan.plan_name,
                        start_date=subscription.start_date,
                        end_date=subscription.end_date
                    )
                )

                print(
                    f"[CANCELLATION EMAIL] "
                    f"Email result: {email_sent}"
                )

                if email_sent:

                    print(
                        f"[CANCELLATION EMAIL SUCCESS] "
                        f"Cancellation email sent to "
                        f"{user.email}"
                    )

                else:

                    print(
                        f"[CANCELLATION EMAIL ERROR] "
                        f"Cancellation email failed for "
                        f"{user.email}"
                    )

            except Exception as email_error:

                print(
                    f"[CANCELLATION EMAIL ERROR] "
                    f"{email_error}"
                )

        else:

            print(
                "[CANCELLATION EMAIL] "
                "No customer email found."
            )

        return updated_subscription

    # ============================================================
    # UPDATE EXPIRED SUBSCRIPTIONS
    # ============================================================

    @staticmethod
    def update_expired_subscriptions(
        db: Session
    ):

        expired_subscriptions = (
            SubscriptionRepository
            .get_expired_active_subscriptions(db)
        )

        updated_count = 0

        for subscription in expired_subscriptions:

            subscription.status = "expired"

            SubscriptionRepository.update_subscription(
                db,
                subscription
            )

            NotificationService.create_notification(
                db=db,
                user_id=subscription.user_id,
                title="Subscription Expired",
                message=(
                    "Your subscription has expired. "
                    "You can renew your subscription "
                    "to continue the service."
                ),
                notification_type="subscription_expired"
            )

            updated_count += 1

        return {
            "message": (
                "Expired subscriptions updated successfully."
            ),
            "updated_count": updated_count
        }

    # ============================================================
    # RENEW EXPIRED SUBSCRIPTION
    # ============================================================

    @staticmethod
    def renew_subscription(
        db: Session,
        subscription_id: int,
        user_id: int
    ):

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

        if old_subscription.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You can only renew your own subscription."
                )
            )

        if old_subscription.status != "expired":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only expired subscriptions "
                    "can be renewed."
                )
            )

        plan = SubscriptionPlanRepository.get_by_id(
            db,
            old_subscription.plan_id
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Subscription plan not found"
            )

        active_subscription = (
            SubscriptionRepository.get_active_subscription(
                db,
                user_id
            )
        )

        if active_subscription:
            raise HTTPException(
                status_code=400,
                detail=(
                    "You already have an active subscription."
                )
            )

        start_date = date.today()

        end_date = (
            start_date
            + timedelta(days=plan.duration_days)
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

    # ============================================================
    # SEND 3-DAY EXPIRY REMINDERS
    # ============================================================

    @staticmethod
    def send_expiry_reminders(
        db: Session
    ):

        target_date = (
            date.today()
            + timedelta(days=3)
        )

        subscriptions = (
            SubscriptionRepository
            .get_subscriptions_expiring_on(
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

            print(
                f"[EXPIRY REMINDER] "
                f"Notification created for "
                f"user_id={subscription.user_id}"
            )

            user = UserRepository.get_by_id(
                db,
                subscription.user_id
            )

            if user and user.email:

                print(
                    f"[EXPIRY EMAIL] "
                    f"Sending expiry reminder to "
                    f"{user.email}"
                )

                try:

                    email_sent = (
                        EmailService
                        .send_subscription_expiry_reminder_email(
                            to_email=user.email,
                            username=user.username,
                            plan_name=plan_name,
                            end_date=subscription.end_date
                        )
                    )

                    print(
                        f"[EXPIRY EMAIL] "
                        f"Email result: {email_sent}"
                    )

                    if email_sent:

                        print(
                            f"[EXPIRY EMAIL SUCCESS] "
                            f"Expiry reminder sent to "
                            f"{user.email}"
                        )

                    else:

                        print(
                            f"[EXPIRY EMAIL ERROR] "
                            f"Expiry reminder failed for "
                            f"{user.email}"
                        )

                except Exception as email_error:

                    print(
                        f"[EXPIRY EMAIL ERROR] "
                        f"{email_error}"
                    )

            else:

                print(
                    "[EXPIRY EMAIL] "
                    "No customer email found."
                )

            reminder_count += 1

        return {
            "message": (
                "Expiry reminders processed successfully."
            ),
            "reminder_count": reminder_count
        }
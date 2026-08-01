from app.database.database import SessionLocal
from app.models.invoice import Invoice
from app.services.subscription_service import SubscriptionService


def check_expired_subscriptions_job():
    db = SessionLocal()

    try:
        # 1. Update subscriptions that have already expired
        expiry_result = (
            SubscriptionService.update_expired_subscriptions(db)
        )

        print(
            f"Automatic expiry check completed. "
            f"Updated: {expiry_result['updated_count']}"
        )

        # 2. Send reminders for subscriptions expiring in 3 days
        reminder_result = (
            SubscriptionService.send_expiry_reminders(db)
        )

        print(
            f"Expiry reminder check completed. "
            f"Reminders sent: {reminder_result['reminder_count']}"
        )

    except Exception as error:
        print(
            f"Automatic subscription job failed: {error}"
        )

    finally:
        db.close()
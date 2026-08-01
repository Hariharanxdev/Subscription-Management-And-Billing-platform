from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    @staticmethod
    def get_admin_summary(db: Session):

        total_users = DashboardRepository.get_total_users(db)

        total_plans = DashboardRepository.get_total_plans(db)

        total_subscriptions = (
            DashboardRepository.get_total_subscriptions(db)
        )

        active_subscriptions = (
            DashboardRepository.get_subscription_count_by_status(
                db,
                "active"
            )
        )

        expired_subscriptions = (
            DashboardRepository.get_subscription_count_by_status(
                db,
                "expired"
            )
        )

        cancelled_subscriptions = (
            DashboardRepository.get_subscription_count_by_status(
                db,
                "cancelled"
            )
        )

        total_payments = DashboardRepository.get_total_payments(db)

        total_revenue = DashboardRepository.get_total_revenue(db)

        total_invoices = DashboardRepository.get_total_invoices(db)

        return {
            "total_users": total_users,
            "total_plans": total_plans,
            "total_subscriptions": total_subscriptions,
            "active_subscriptions": active_subscriptions,
            "expired_subscriptions": expired_subscriptions,
            "cancelled_subscriptions": cancelled_subscriptions,
            "total_payments": total_payments,
            "total_revenue": total_revenue,
            "total_invoices": total_invoices
        }

    @staticmethod
    def get_recent_payments(
        db: Session,
        limit: int = 5
    ):
        return DashboardRepository.get_recent_payments(
            db,
            limit
        )

    @staticmethod
    def get_recent_subscriptions(
        db: Session,
        limit: int = 5
    ):
        return DashboardRepository.get_recent_subscriptions(
            db,
            limit
        )


    @staticmethod
    def get_revenue_report(db: Session):
        successful_payments = (
            DashboardRepository.get_successful_payments(db)
        )

        total_revenue = sum(
            payment.amount for payment in successful_payments
        )

        successful_payment_count = len(successful_payments)

        average_payment = (
            total_revenue / successful_payment_count
            if successful_payment_count > 0
            else 0
        )

        return {
            "total_revenue": round(total_revenue, 2),
            "successful_payments": successful_payment_count,
            "average_payment": round(average_payment, 2)
        }

        # -------------------------------------------------
    # CUSTOMER DASHBOARD SUMMARY
    # -------------------------------------------------
    @staticmethod
    def get_customer_summary(
        db: Session,
        user_id: int
    ):
        # Get customer's active subscription
        active_subscription = (
            DashboardRepository.get_customer_active_subscription(
                db,
                user_id
            )
        )

        # Get customer's successful payments
        payments = (
            DashboardRepository.get_customer_successful_payments(
                db,
                user_id
            )
        )

        total_payments = len(payments)

        total_amount_paid = sum(
            payment.amount for payment in payments
        )

        # Get customer's invoice count
        total_invoices = (
            DashboardRepository.get_customer_invoice_count(
                db,
                user_id
            )
        )

        # Prepare active subscription details
        subscription_data = None

        if active_subscription:
            plan = active_subscription.plan

            subscription_data = {
                "subscription_id": active_subscription.id,
                "plan_id": active_subscription.plan_id,
                "plan_name": plan.plan_name,
                "price": plan.price,
                "status": active_subscription.status,
                "start_date": active_subscription.start_date,
                "end_date": active_subscription.end_date
            }

        return {
            "user_id": user_id,
            "active_subscription": subscription_data,
            "total_payments": total_payments,
            "total_amount_paid": round(total_amount_paid, 2),
            "total_invoices": total_invoices
        }
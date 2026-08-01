from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.dashboard_service import DashboardService
from app.core.dependencies import get_current_admin
from app.core.security import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, Query


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Admin - Dashboard summary
@router.get("/admin/summary")
def get_admin_dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_admin_summary(db)


# Admin - View recent payments
@router.get("/admin/recent-payments")
def get_recent_payments(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_recent_payments(
        db,
        limit
    )


# Admin - View recent subscriptions
@router.get("/admin/recent-subscriptions")
def get_recent_subscriptions(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_recent_subscriptions(
        db,
        limit
    )


# Admin - Revenue report
@router.get("/admin/revenue")
def get_revenue_report(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_revenue_report(db)


# Customer - Dashboard summary
@router.get("/customer/summary")
def get_customer_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DashboardService.get_customer_summary(
        db,
        current_user.id
    )

# Admin - View recent payments
@router.get("/admin/recent-payments")
def get_recent_payments(
    limit: int = Query(default=5, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_recent_payments(
        db,
        limit
    )


# Admin - View recent subscriptions
@router.get("/admin/recent-subscriptions")
def get_recent_subscriptions(
    limit: int = Query(default=5, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return DashboardService.get_recent_subscriptions(
        db,
        limit
    )
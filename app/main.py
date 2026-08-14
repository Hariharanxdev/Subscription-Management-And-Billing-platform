from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.auth import router as auth_router
from app.api.subscription_plan import router as subscription_plan_router
from app.api.subscription import router as subscription_router
from app.api.payment import router as payment_router
from app.api.invoice import router as invoice_router
from app.api.dashboard import router as dashboard_router
from app.api.notification import router as notification_router
from app.api.admin_user import router as admin_user_router
from app.api.profile import router as profile_router
from app.api.email_test import router as email_test_router

from fastapi.middleware.cors import CORSMiddleware

from app.jobs.subscription_jobs import check_expired_subscriptions_job


# Create scheduler
scheduler = BackgroundScheduler(
    timezone="Asia/Kolkata"
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Run subscription expiry check every day at 12:05 AM
    scheduler.add_job(
        check_expired_subscriptions_job,
        trigger="cron",
        hour=0,
        minute=5,
        id="subscription_expiry_job",
        replace_existing=True
    )

    scheduler.start()

    print("Subscription expiry scheduler started.")

    yield

    scheduler.shutdown()

    print("Subscription expiry scheduler stopped.")


app = FastAPI(
    title="Subscription Management and Automated Billing Platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(subscription_plan_router)
app.include_router(subscription_router)
app.include_router(payment_router)
app.include_router(invoice_router)
app.include_router(dashboard_router)
app.include_router(notification_router)
app.include_router(admin_user_router)
app.include_router(profile_router)
app.include_router(email_test_router)


@app.get("/")
def root():
    return {
        "message": "Backend is running successfully!"
    }
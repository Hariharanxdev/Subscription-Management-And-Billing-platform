from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.email_service import EmailService


router = APIRouter()


class EmailTestRequest(BaseModel):
    to_email: str


@router.post("/email-test")
def test_email(request: EmailTestRequest):

    success = EmailService.send_email(
        to_email=request.to_email,
        subject="BillPro Email Test",
        html_body="""
        <html>
            <body>
                <h1>BillPro Email Test 🎉</h1>

                <p>Hello!</p>

                <p>
                    This is a test email from the
                    <strong>BillPro</strong> platform.
                </p>

                <p>
                    Your Brevo SMTP integration is working successfully.
                </p>

                <p>
                    Regards,<br>
                    <strong>BillPro Team</strong>
                </p>
            </body>
        </html>
        """,
        text_body="""
BillPro Email Test

Hello!

This is a test email from the BillPro platform.

Your Brevo SMTP integration is working successfully.

Regards,
BillPro Team
"""
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send test email."
        )

    return {
        "message": "Test email sent successfully.",
        "to": request.to_email
    }
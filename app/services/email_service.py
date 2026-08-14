'''import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.settings import settings


logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str | None = None
    ) -> bool:

        # Check SMTP configuration
        if not settings.SMTP_HOST:
            logger.error("SMTP_HOST is not configured.")
            return False

        if not settings.SMTP_USERNAME:
            logger.error("SMTP_USERNAME is not configured.")
            return False

        if not settings.SMTP_PASSWORD:
            logger.error("SMTP_PASSWORD is not configured.")
            return False

        if not settings.SMTP_FROM_EMAIL:
            logger.error("SMTP_FROM_EMAIL is not configured.")
            return False

        try:
            # Create email message
            message = MIMEMultipart("alternative")

            message["From"] = (
                f"{settings.SMTP_FROM_NAME} "
                f"<{settings.SMTP_FROM_EMAIL}>"
            )

            message["To"] = to_email
            message["Subject"] = subject

            # Plain text version
            if text_body:
                message.attach(
                    MIMEText(
                        text_body,
                        "plain",
                        "utf-8"
                    )
                )

            # HTML version
            message.attach(
                MIMEText(
                    html_body,
                    "html",
                    "utf-8"
                )
            )

            # Connect to Brevo SMTP
            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT
            ) as server:

                # Enable TLS
                if settings.SMTP_USE_TLS:
                    server.starttls()

                # Authenticate
                server.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD
                )

                # Send email
                server.sendmail(
                    settings.SMTP_FROM_EMAIL,
                    to_email,
                    message.as_string()
                )

            logger.info(
                "Email sent successfully to %s",
                to_email
            )

            return True

        except Exception:
            logger.exception(
                "Failed to send email to %s",
                to_email
            )

            return False

    # ============================================================
    # WELCOME EMAIL
    # ============================================================

    @staticmethod
    def send_welcome_email(
        to_email: str,
        username: str
    ) -> bool:

        subject = "Welcome to BillPro 🎉"

        text_body = f"""
Hello {username},

Welcome to BillPro!

Your BillPro account has been successfully created.

You can now manage your subscriptions, payments,
invoices and billing information from your dashboard.

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome to BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Welcome to BillPro 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro account has been successfully created.
        </p>

        <p>
            You can now manage your:
        </p>

        <ul>
            <li>Subscriptions</li>
            <li>Payments</li>
            <li>Invoices</li>
            <li>Billing information</li>
        </ul>

        <p>
            Thank you for choosing BillPro.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

    # ============================================================
    # PAYMENT SUCCESS EMAIL
    # ============================================================

    @staticmethod
    def send_payment_success_email(
        to_email: str,
        username: str,
        amount: float,
        plan_name: str,
        transaction_id: str,
        payment_method: str
    ) -> bool:

        subject = "Payment Successful - BillPro"

        text_body = f"""
Hello {username},

Your payment has been successfully completed.

Payment Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: Successful

Your invoice has also been generated.

Thank you for using BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Successful - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Payment Successful 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your payment has been successfully completed.
        </p>

        <h3>
            Payment Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>

                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>

                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>

                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    font-weight: bold;
                ">
                    Successful
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Your invoice has also been generated.
        </p>

        <p>
            Thank you for using <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

            # ============================================================
    # PAYMENT FAILED EMAIL
    # ============================================================

    @staticmethod
    def send_payment_failed_email(
        to_email: str,
        username: str,
        amount: float,
        plan_name: str,
        transaction_id: str,
        payment_method: str
    ) -> bool:

        subject = "Payment Failed - BillPro"

        text_body = f"""
Hello {username},

Unfortunately, your payment could not be completed.

Payment Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: Failed

Please try the payment again or use another payment method.

If money was deducted from your account, please contact your payment provider or BillPro support.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Failed - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #dc2626;">
            Payment Failed ❌
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Unfortunately, your payment could not be completed.
        </p>

        <h3>
            Payment Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>

                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>

                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>

                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    font-weight: bold;
                    color: #dc2626;
                ">
                    Failed
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Please try the payment again or use another payment method.
        </p>

        <p>
            If money was deducted from your account,
            please contact your payment provider or BillPro support.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

            # ============================================================
    # INVOICE GENERATED EMAIL
    # ============================================================

    @staticmethod
    def send_invoice_generated_email(
        to_email: str,
        username: str,
        invoice_number: str,
        amount: float,
        transaction_id: str,
        payment_method: str,
        status: str
    ) -> bool:

        subject = f"Invoice {invoice_number} - BillPro"

        text_body = f"""
Hello {username},

Your BillPro invoice has been generated successfully.

Invoice Details
-------------------------
Invoice Number: {invoice_number}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: {status}

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice Generated - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Invoice Generated 🧾
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro invoice has been generated successfully.
        </p>

        <h3>
            Invoice Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Invoice Number</strong>
                </td>
                <td style="padding: 10px 0;">
                    {invoice_number}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>
                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>
                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>
                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>
                <td style="
                    padding: 10px 0;
                    color: #16a34a;
                    font-weight: bold;
                ">
                    {status}
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Thank you for choosing <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )


            # ============================================================
    # SUBSCRIPTION ACTIVATED EMAIL
    # ============================================================

    @staticmethod
    def send_subscription_activated_email(
        to_email: str,
        username: str,
        plan_name: str,
        amount: float,
        start_date,
        end_date
    ) -> bool:

        subject = "Subscription Activated - BillPro"

        text_body = f"""
Hello {username},

Your BillPro subscription has been activated successfully.

Subscription Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Start Date: {start_date}
End Date: {end_date}
Status: Active

You can now use your BillPro subscription.

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Subscription Activated - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #16a34a;">
            Subscription Activated 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro subscription has been
            activated successfully.
        </p>

        <h3>
            Subscription Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>
                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>
                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Start Date</strong>
                </td>
                <td style="padding: 10px 0;">
                    {start_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>End Date</strong>
                </td>
                <td style="padding: 10px 0;">
                    {end_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>
                <td style="
                    padding: 10px 0;
                    color: #16a34a;
                    font-weight: bold;
                ">
                    Active
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            You can now use your BillPro subscription.
        </p>

        <p>
            Thank you for choosing <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
        # ============================================================
# SUBSCRIPTION EXPIRY REMINDER EMAIL
# ============================================================

@staticmethod
def send_subscription_expiry_reminder_email(
    to_email: str,
    username: str,
    plan_name: str,
    end_date
) -> bool:

    subject = "Subscription Expiring Soon - BillPro"

    text_body = f"""
Hello {username},

Your BillPro subscription is expiring soon.

Subscription Details
-------------------------
Plan: {plan_name}
Expiry Date: {end_date}
Status: Active

Your subscription will expire in 3 days.

Please renew your subscription to continue using BillPro
without interruption.

Regards,
BillPro Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Subscription Expiring Soon - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #d97706;">
            Subscription Expiring Soon ⚠️
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro subscription is expiring soon.
        </p>

        <h3>Subscription Details</h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Expiry Date</strong>
                </td>

                <td style="padding: 10px 0;">
                    {end_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    color: #16a34a;
                    font-weight: bold;
                ">
                    Active
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Your subscription will expire in
            <strong>3 days</strong>.
        </p>

        <p>
            Please renew your subscription to continue
            using BillPro without interruption.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

    return EmailService.send_email(
        to_email=to_email,
        subject=subject,
        html_body=html_body,
        text_body=text_body
    )
    # ============================================================
    # SUBSCRIPTION CANCELLED EMAIL
    # ============================================================

@staticmethod
def send_subscription_cancelled_email(
        to_email: str,
        username: str,
        plan_name: str,
        start_date,
        end_date
    ) -> bool:

        subject = "Subscription Cancelled - BillPro"

        text_body = f"""
Hello {username},

Your BillPro subscription has been cancelled successfully.

Subscription Details
-------------------------
Plan: {plan_name}
Start Date: {start_date}
End Date: {end_date}
Status: Cancelled

Your subscription is no longer active.

If you cancelled this subscription by mistake,
you can create a new subscription from your BillPro dashboard.

Thank you for using BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Subscription Cancelled - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #dc2626;">
            Subscription Cancelled
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro subscription has been
            cancelled successfully.
        </p>

        <h3>
            Subscription Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Start Date</strong>
                </td>

                <td style="padding: 10px 0;">
                    {start_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>End Date</strong>
                </td>

                <td style="padding: 10px 0;">
                    {end_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    color: #dc2626;
                    font-weight: bold;
                ">
                    Cancelled
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Your subscription is no longer active.
        </p>

        <p>
            If you cancelled this subscription by mistake,
            you can create a new subscription from your
            BillPro dashboard.
        </p>

        <p>
            Thank you for using <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

'''

import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.settings import settings


logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str | None = None
    ) -> bool:

        # Check SMTP configuration
        if not settings.SMTP_HOST:
            logger.error("SMTP_HOST is not configured.")
            return False

        if not settings.SMTP_USERNAME:
            logger.error("SMTP_USERNAME is not configured.")
            return False

        if not settings.SMTP_PASSWORD:
            logger.error("SMTP_PASSWORD is not configured.")
            return False

        if not settings.SMTP_FROM_EMAIL:
            logger.error("SMTP_FROM_EMAIL is not configured.")
            return False

        try:
            # Create email message
            message = MIMEMultipart("alternative")

            message["From"] = (
                f"{settings.SMTP_FROM_NAME} "
                f"<{settings.SMTP_FROM_EMAIL}>"
            )

            message["To"] = to_email
            message["Subject"] = subject

            # Plain text version
            if text_body:
                message.attach(
                    MIMEText(
                        text_body,
                        "plain",
                        "utf-8"
                    )
                )

            # HTML version
            message.attach(
                MIMEText(
                    html_body,
                    "html",
                    "utf-8"
                )
            )

            # Connect to Brevo SMTP
            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT
            ) as server:

                # Enable TLS
                if settings.SMTP_USE_TLS:
                    server.starttls()

                # Authenticate
                server.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD
                )

                # Send email
                server.sendmail(
                    settings.SMTP_FROM_EMAIL,
                    to_email,
                    message.as_string()
                )

            logger.info(
                "Email sent successfully to %s",
                to_email
            )

            return True

        except Exception:
            logger.exception(
                "Failed to send email to %s",
                to_email
            )

            return False

    # ============================================================
    # WELCOME EMAIL
    # ============================================================

    @staticmethod
    def send_welcome_email(
        to_email: str,
        username: str
    ) -> bool:

        subject = "Welcome to BillPro 🎉"

        text_body = f"""
Hello {username},

Welcome to BillPro!

Your BillPro account has been successfully created.

You can now manage your subscriptions, payments,
invoices and billing information from your dashboard.

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome to BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Welcome to BillPro 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro account has been successfully created.
        </p>

        <p>
            You can now manage your:
        </p>

        <ul>
            <li>Subscriptions</li>
            <li>Payments</li>
            <li>Invoices</li>
            <li>Billing information</li>
        </ul>

        <p>
            Thank you for choosing BillPro.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

    # ============================================================
    # PAYMENT SUCCESS EMAIL
    # ============================================================

    @staticmethod
    def send_payment_success_email(
        to_email: str,
        username: str,
        amount: float,
        plan_name: str,
        transaction_id: str,
        payment_method: str
    ) -> bool:

        subject = "Payment Successful - BillPro"

        text_body = f"""
Hello {username},

Your payment has been successfully completed.

Payment Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: Successful

Your invoice has also been generated.

Thank you for using BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Successful - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Payment Successful 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your payment has been successfully completed.
        </p>

        <h3>
            Payment Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>

                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>

                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>

                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    font-weight: bold;
                ">
                    Successful
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Your invoice has also been generated.
        </p>

        <p>
            Thank you for using <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

            # ============================================================
    # PAYMENT FAILED EMAIL
    # ============================================================

    @staticmethod
    def send_payment_failed_email(
        to_email: str,
        username: str,
        amount: float,
        plan_name: str,
        transaction_id: str,
        payment_method: str
    ) -> bool:

        subject = "Payment Failed - BillPro"

        text_body = f"""
Hello {username},

Unfortunately, your payment could not be completed.

Payment Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: Failed

Please try the payment again or use another payment method.

If money was deducted from your account, please contact your payment provider or BillPro support.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Failed - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #dc2626;">
            Payment Failed ❌
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Unfortunately, your payment could not be completed.
        </p>

        <h3>
            Payment Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>

                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>

                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>

                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>

                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>

                <td style="
                    padding: 10px 0;
                    font-weight: bold;
                    color: #dc2626;
                ">
                    Failed
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Please try the payment again or use another payment method.
        </p>

        <p>
            If money was deducted from your account,
            please contact your payment provider or BillPro support.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )

            # ============================================================
    # INVOICE GENERATED EMAIL
    # ============================================================

    @staticmethod
    def send_invoice_generated_email(
        to_email: str,
        username: str,
        invoice_number: str,
        amount: float,
        transaction_id: str,
        payment_method: str,
        status: str
    ) -> bool:

        subject = f"Invoice {invoice_number} - BillPro"

        text_body = f"""
Hello {username},

Your BillPro invoice has been generated successfully.

Invoice Details
-------------------------
Invoice Number: {invoice_number}
Amount: ₹{amount:.2f}
Transaction ID: {transaction_id}
Payment Method: {payment_method}
Status: {status}

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice Generated - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #111827;">
            Invoice Generated 🧾
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro invoice has been generated successfully.
        </p>

        <h3>
            Invoice Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Invoice Number</strong>
                </td>
                <td style="padding: 10px 0;">
                    {invoice_number}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>
                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Transaction ID</strong>
                </td>
                <td style="padding: 10px 0;">
                    {transaction_id}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Payment Method</strong>
                </td>
                <td style="padding: 10px 0;">
                    {payment_method}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>
                <td style="
                    padding: 10px 0;
                    color: #16a34a;
                    font-weight: bold;
                ">
                    {status}
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            Thank you for choosing <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )


            # ============================================================
    # SUBSCRIPTION ACTIVATED EMAIL
    # ============================================================

    @staticmethod
    def send_subscription_activated_email(
        to_email: str,
        username: str,
        plan_name: str,
        amount: float,
        start_date,
        end_date
    ) -> bool:

        subject = "Subscription Activated - BillPro"

        text_body = f"""
Hello {username},

Your BillPro subscription has been activated successfully.

Subscription Details
-------------------------
Plan: {plan_name}
Amount: ₹{amount:.2f}
Start Date: {start_date}
End Date: {end_date}
Status: Active

You can now use your BillPro subscription.

Thank you for choosing BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Subscription Activated - BillPro</title>
</head>

<body style="
    margin: 0;
    padding: 40px;
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
">

    <div style="
        max-width: 600px;
        margin: auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
    ">

        <h1 style="color: #16a34a;">
            Subscription Activated 🎉
        </h1>

        <p>
            Hello <strong>{username}</strong>,
        </p>

        <p>
            Your BillPro subscription has been
            activated successfully.
        </p>

        <h3>
            Subscription Details
        </h3>

        <table style="
            width: 100%;
            border-collapse: collapse;
        ">

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Plan</strong>
                </td>
                <td style="padding: 10px 0;">
                    {plan_name}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Amount</strong>
                </td>
                <td style="padding: 10px 0;">
                    ₹{amount:.2f}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Start Date</strong>
                </td>
                <td style="padding: 10px 0;">
                    {start_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>End Date</strong>
                </td>
                <td style="padding: 10px 0;">
                    {end_date}
                </td>
            </tr>

            <tr>
                <td style="padding: 10px 0;">
                    <strong>Status</strong>
                </td>
                <td style="
                    padding: 10px 0;
                    color: #16a34a;
                    font-weight: bold;
                ">
                    Active
                </td>
            </tr>

        </table>

        <p style="margin-top: 30px;">
            You can now use your BillPro subscription.
        </p>

        <p>
            Thank you for choosing <strong>BillPro</strong>.
        </p>

        <p>
            Regards,<br>
            <strong>BillPro Team</strong>
        </p>

    </div>

</body>
</html>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
    # ============================================================
    # SUBSCRIPTION EXPIRY REMINDER EMAIL
    # ============================================================

    @staticmethod
    def send_subscription_expiry_reminder_email(
        to_email: str,
        username: str,
        plan_name: str,
        end_date
    ) -> bool:

        subject = "Subscription Expiring Soon - BillPro"

        text_body = f"""
    Hello {username},

    Your BillPro subscription is expiring soon.

    Subscription Details
    -------------------------
    Plan: {plan_name}
    Expiry Date: {end_date}
    Status: Active

    Your subscription will expire in 3 days.

    Please renew your subscription to continue using BillPro
    without interruption.

    Regards,
    BillPro Team
    """

        html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Subscription Expiring Soon - BillPro</title>
    </head>

    <body style="
        margin: 0;
        padding: 40px;
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
    ">

        <div style="
            max-width: 600px;
            margin: auto;
            background-color: #ffffff;
            padding: 40px;
            border-radius: 12px;
        ">

            <h1 style="color: #d97706;">
                Subscription Expiring Soon ⚠️
            </h1>

            <p>
                Hello <strong>{username}</strong>,
            </p>

            <p>
                Your BillPro subscription is expiring soon.
            </p>

            <h3>Subscription Details</h3>

            <table style="
                width: 100%;
                border-collapse: collapse;
            ">

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Plan</strong>
                    </td>

                    <td style="padding: 10px 0;">
                        {plan_name}
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Expiry Date</strong>
                    </td>

                    <td style="padding: 10px 0;">
                        {end_date}
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Status</strong>
                    </td>

                    <td style="
                        padding: 10px 0;
                        color: #16a34a;
                        font-weight: bold;
                    ">
                        Active
                    </td>
                </tr>

            </table>

            <p style="margin-top: 30px;">
                Your subscription will expire in
                <strong>3 days</strong>.
            </p>

            <p>
                Please renew your subscription to continue
                using BillPro without interruption.
            </p>

            <p>
                Regards,<br>
                <strong>BillPro Team</strong>
            </p>

        </div>

    </body>
    </html>
    """

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
        # ============================================================
        # SUBSCRIPTION CANCELLED EMAIL
        # ============================================================

    @staticmethod
    def send_subscription_cancelled_email(
            to_email: str,
            username: str,
            plan_name: str,
            start_date,
            end_date
        ) -> bool:

            subject = "Subscription Cancelled - BillPro"

            text_body = f"""
    Hello {username},

    Your BillPro subscription has been cancelled successfully.

    Subscription Details
    -------------------------
    Plan: {plan_name}
    Start Date: {start_date}
    End Date: {end_date}
    Status: Cancelled

    Your subscription is no longer active.

    If you cancelled this subscription by mistake,
    you can create a new subscription from your BillPro dashboard.

    Thank you for using BillPro.

    Regards,
    BillPro Team
    """

            html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Subscription Cancelled - BillPro</title>
    </head>

    <body style="
        margin: 0;
        padding: 40px;
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
    ">

        <div style="
            max-width: 600px;
            margin: auto;
            background-color: #ffffff;
            padding: 40px;
            border-radius: 12px;
        ">

            <h1 style="color: #dc2626;">
                Subscription Cancelled
            </h1>

            <p>
                Hello <strong>{username}</strong>,
            </p>

            <p>
                Your BillPro subscription has been
                cancelled successfully.
            </p>

            <h3>
                Subscription Details
            </h3>

            <table style="
                width: 100%;
                border-collapse: collapse;
            ">

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Plan</strong>
                    </td>

                    <td style="padding: 10px 0;">
                        {plan_name}
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Start Date</strong>
                    </td>

                    <td style="padding: 10px 0;">
                        {start_date}
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>End Date</strong>
                    </td>

                    <td style="padding: 10px 0;">
                        {end_date}
                    </td>
                </tr>

                <tr>
                    <td style="padding: 10px 0;">
                        <strong>Status</strong>
                    </td>

                    <td style="
                        padding: 10px 0;
                        color: #dc2626;
                        font-weight: bold;
                    ">
                        Cancelled
                    </td>
                </tr>

            </table>

            <p style="margin-top: 30px;">
                Your subscription is no longer active.
            </p>

            <p>
                If you cancelled this subscription by mistake,
                you can create a new subscription from your
                BillPro dashboard.
            </p>

            <p>
                Thank you for using <strong>BillPro</strong>.
            </p>

            <p>
                Regards,<br>
                <strong>BillPro Team</strong>
            </p>

        </div>

    </body>
    </html>
    """

            return EmailService.send_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body
            )

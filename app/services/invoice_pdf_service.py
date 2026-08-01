from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class InvoicePDFService:

    @staticmethod
    def generate_invoice_pdf(
        invoice,
        payment,
        subscription,
        plan,
        user
    ):
        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = styles["Title"]
        title_style.alignment = TA_CENTER

        elements.append(
            Paragraph(
                "Subscription Management & Automated Billing Platform",
                title_style
            )
        )

        elements.append(Spacer(1, 20))

        invoice_style = styles["Heading1"]
        invoice_style.alignment = TA_CENTER

        elements.append(
            Paragraph("INVOICE", invoice_style)
        )

        elements.append(Spacer(1, 25))

        # Invoice information
        invoice_info = [
            ["Invoice Number", invoice.invoice_number],
            ["Invoice Date", str(invoice.issued_at.date())],
            ["Customer", user.email],
            ["Plan", plan.plan_name],
            ["Billing Cycle", plan.billing_cycle],
        ]

        info_table = Table(
            invoice_info,
            colWidths=[150, 300]
        )

        info_table.setStyle(
            TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ])
        )

        elements.append(info_table)

        elements.append(Spacer(1, 30))

        # Payment details
        payment_data = [
            ["Description", "Amount"],
            [f"{plan.plan_name} Subscription", f"Rs. {payment.amount:.2f}"],
            ["Total", f"Rs. {payment.amount:.2f}"]
        ]

        payment_table = Table(
            payment_data,
            colWidths=[330, 120]
        )

        payment_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ])
        )

        elements.append(payment_table)

        elements.append(Spacer(1, 30))

        # Transaction details
        transaction_data = [
            ["Payment Method", payment.payment_method],
            ["Transaction ID", payment.transaction_id],
            ["Payment Status", payment.payment_status.upper()],
        ]

        transaction_table = Table(
            transaction_data,
            colWidths=[150, 300]
        )

        transaction_table.setStyle(
            TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ])
        )

        elements.append(transaction_table)

        elements.append(Spacer(1, 40))

        footer_style = styles["Normal"]
        footer_style.alignment = TA_CENTER

        elements.append(
            Paragraph(
                "Thank you for your payment.",
                footer_style
            )
        )

        document.build(elements)

        buffer.seek(0)

        return buffer
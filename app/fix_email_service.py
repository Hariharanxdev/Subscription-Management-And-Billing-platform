import ast

FILE = "app/services/email_service.py"

with open(FILE, "r", encoding="utf-8") as f:
    source = f.read()

tree = ast.parse(source)

# Find EmailService class
email_class = None

for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == "EmailService":
        email_class = node
        break

if email_class is None:
    raise RuntimeError("EmailService class was not found.")

# Find duplicate cancellation methods that are OUTSIDE EmailService
remove_ranges = []

for node in tree.body:
    if (
        isinstance(node, ast.FunctionDef)
        and node.name == "send_subscription_cancelled_email"
    ):
        remove_ranges.append(
            (node.lineno - 1, node.end_lineno)
        )

# Remove duplicate top-level methods
lines = source.splitlines()

for start, end in reversed(remove_ranges):
    del lines[start:end]

source = "\n".join(lines)

# Parse cleaned source
tree = ast.parse(source)

email_class = None

for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == "EmailService":
        email_class = node
        break

if email_class is None:
    raise RuntimeError(
        "EmailService class was not found after cleanup."
    )

# Correct cancellation email method
method = '''
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

Plan: {plan_name}
Start Date: {start_date}
End Date: {end_date}
Status: Cancelled

Thank you for using BillPro.

Regards,
BillPro Team
"""

        html_body = f"""
<h1>Subscription Cancelled - BillPro</h1>

<p>Hello <strong>{username}</strong>,</p>

<p>
Your BillPro subscription has been cancelled successfully.
</p>

<p>
<strong>Plan:</strong> {plan_name}
</p>

<p>
<strong>Start Date:</strong> {start_date}
</p>

<p>
<strong>End Date:</strong> {end_date}
</p>

<p>
<strong>Status:</strong>
<span style="color: red;">Cancelled</span>
</p>

<p>
Thank you for using <strong>BillPro</strong>.
</p>

<p>
Regards,<br>
<strong>BillPro Team</strong>
</p>
"""

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
'''

# Recalculate class end
class_end_line = email_class.end_lineno

lines = source.splitlines()

# Add the correct method inside EmailService
lines.insert(
    class_end_line - 1,
    method.strip("\n")
)

fixed_source = "\n".join(lines) + "\n"

# Validate before saving
ast.parse(fixed_source)

# Create backup
with open(
    FILE + ".backup",
    "w",
    encoding="utf-8"
) as f:
    f.write(source)

# Save fixed file
with open(
    FILE,
    "w",
    encoding="utf-8"
) as f:
    f.write(fixed_source)

print("EmailService fixed successfully.")
print("Backup created:")
print(FILE + ".backup")
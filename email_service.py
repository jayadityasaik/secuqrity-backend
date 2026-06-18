import smtplib
import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def generate_otp():
    return str(random.randint(100000, 999999))


def send_email_otp(receiver_email, otp, role="user"):

    subject = "secuQRity OTP Verification"

    if role == "authenticator":
        body = f"WELCOME AUTHENTICATOR\n\nYour OTP is:\n\n{otp}\n\nValid for 5 minutes only."

    elif role == "admin":
        body = f"WELCOME ADMIN\n\nYour OTP is:\n\n{otp}\n\nValid for 5 minutes only."

    else:
        body = f"WELCOME TO secuQRity\n\nYour OTP is:\n\n{otp}\n\nValid for 5 minutes only."

    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.sendmail(
        EMAIL_ADDRESS,
        receiver_email,
        message.as_string()
    )

    server.quit()


def send_authenticator_credentials(
    receiver_email,
    authenticator_id,
    password
):

    try:

        subject = (
            "Your secuQRity Authenticator Credentials"
        )

        body = f"""
Hello,

Your Authenticator Account has been created successfully.

==================================

Authenticator ID:
{authenticator_id}

Password:
{password}

==================================

Use these credentials to login
to the secuQRity Authenticator Portal.

Regards,
secuQRity Team
"""

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(
            MIMEText(body, "plain")
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            receiver_email,
            message.as_string()
        )

        server.quit()

        print(
            f"[SUCCESS] Authenticator credentials sent to {receiver_email}"
        )

    except Exception as e:

        print(
            f"[EMAIL ERROR] {str(e)}"
        )


def send_user_credentials(
    receiver_email,
    password,
    biometric_token
):

    subject = "Your secuQRity User Credentials"

    body = f"""
Hello,

Your secuQRity User Account has been created.

Email:
{receiver_email}

Password:
{password}

Biometric Token:
{biometric_token}

Give this Biometric Token to an Authenticator
for biometric enrollment.

Regards,
secuQRity Team
"""

    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.sendmail(
        EMAIL_ADDRESS,
        receiver_email,
        message.as_string()
    )

    server.quit()
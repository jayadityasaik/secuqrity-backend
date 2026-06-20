import random
import resend

from config import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def generate_otp():
    return str(random.randint(100000, 999999))


def send_email(receiver_email, subject, body):

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": receiver_email,
        "subject": subject,
        "text": body
    })


def send_email_otp(receiver_email, otp, role="user"):

    subject = "secuQRity OTP Verification"

    if role == "authenticator":

        body = (
            f"WELCOME AUTHENTICATOR\n\n"
            f"Your OTP is:\n\n{otp}\n\n"
            "Valid for 5 minutes only."
        )

    elif role == "admin":

        body = (
            f"WELCOME ADMIN\n\n"
            f"Your OTP is:\n\n{otp}\n\n"
            "Valid for 5 minutes only."
        )

    else:

        body = (
            f"WELCOME TO secuQRity\n\n"
            f"Your OTP is:\n\n{otp}\n\n"
            "Valid for 5 minutes only."
        )

    send_email(
        receiver_email,
        subject,
        body
    )


def send_authenticator_credentials(
    receiver_email,
    authenticator_id,
    password
):

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

    send_email(
        receiver_email,
        subject,
        body
    )


def send_user_credentials(
    email,
    password,
    biometric_token
):

    try:

        resend.Emails.send({

            "from":
            "onboarding@resend.dev",

            "to":
            email,

            "subject":
            "secuQRity Registration",

            "html":
            f"""
            <h2>Registration Successful</h2>

            <p>Email: {email}</p>

            <p>Password: {password}</p>

            <p>Biometric Token:
            {biometric_token}</p>
            """
        })

        print(
            "EMAIL SENT SUCCESSFULLY"
        )

    except Exception as e:

        print(
            "EMAIL FAILED:",
            str(e)
        )

    subject = (
        "Your secuQRity User Credentials"
    )

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

    send_email(
        receiver_email,
        subject,
        body
    )
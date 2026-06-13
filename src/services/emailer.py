# filepath: src/services/emailer.py

"""Email delivery behind a backend seam.

- console (default): logs instead of sending — dev and tests.
- smtp: real delivery via STARTTLS. Activated by EMAIL_BACKEND=smtp plus
  SMTP_* settings; switching is a config change only.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings

logger = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    pass


def send_email(to: str, subject: str, body: str) -> None:
    if settings.EMAIL_BACKEND == "smtp":
        _send_smtp(to, subject, body)
        return
    logger.info("EMAIL (console) to=%s subject=%r body=%r", to, subject, body)


def _send_smtp(to: str, subject: str, body: str) -> None:
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise EmailDeliveryError(
            "EMAIL_BACKEND=smtp but SMTP_HOST/SMTP_USER/SMTP_PASSWORD are not all set"
        )
    sender = settings.EMAIL_FROM or settings.SMTP_USER

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except (smtplib.SMTPException, OSError) as e:
        raise EmailDeliveryError(f"SMTP delivery failed: {e}") from None


def send_verification_email(to: str, token: str) -> None:
    link = f"{settings.PUBLIC_BASE_URL}/auth/verify-email?token={token}"
    send_email(to, "Verify your Crowdjump email", f"Click to verify: {link}")


def send_password_reset_email(to: str, token: str) -> None:
    send_email(to, "Reset your Crowdjump password", f"Your reset token: {token}")

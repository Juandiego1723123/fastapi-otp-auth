"""Envío del código OTP por correo usando smtplib."""

import logging
import smtplib
from email.message import EmailMessage

from app.config import EMAIL_DEV_MODE, OTP_EXPIRE_MINUTES, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER

logger = logging.getLogger(__name__)


def send_otp_email(to_email: str, code: str) -> None:
    """Envía el código OTP al correo del usuario."""
    if EMAIL_DEV_MODE:
        print(f"[DEV] OTP para {to_email}: {code}")
        return

    msg = EmailMessage()
    msg["Subject"] = "Código de verificación"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(f"Tu código de verificación es: {code}\nVence en {OTP_EXPIRE_MINUTES} minutos.")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    logger.info("Correo OTP enviado")

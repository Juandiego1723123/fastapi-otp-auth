"""Generación y validación de códigos OTP."""

from datetime import datetime, timedelta

import pyotp
from sqlalchemy.orm import Session

from app.config import OTP_EXPIRE_MINUTES
from app.models import OTPCode


def generate_code() -> str:
    """Genera un código de 6 dígitos con PyOTP usando un secreto aleatorio."""
    secret = pyotp.random_base32()
    return pyotp.HOTP(secret).at(0)


def create_otp(db: Session, user_id: int) -> str:
    """Invalida los OTP anteriores del usuario y guarda uno nuevo de 15 minutos."""
    db.query(OTPCode).filter(OTPCode.user_id == user_id, OTPCode.used == False).update(  # noqa: E712
        {"used": True}
    )
    code = generate_code()
    otp = OTPCode(
        user_id=user_id,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
    )
    db.add(otp)
    db.commit()
    return code


def verify_otp(db: Session, user_id: int, code: str) -> bool:
    """Valida que el código exista, no esté usado y no haya expirado. Luego lo marca como usado."""
    otp = (
        db.query(OTPCode)
        .filter(OTPCode.user_id == user_id, OTPCode.code == code, OTPCode.used == False)  # noqa: E712
        .first()
    )
    if otp is None or otp.expires_at < datetime.utcnow():
        return False

    otp.used = True
    db.commit()
    return True

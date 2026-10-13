"""Tests unitarios."""

from datetime import datetime, timedelta

from app.models import OTPCode, User
from app.services import otp_service
from app.services.security import create_access_token, decode_access_token, hash_password, verify_password


def create_user(db):
    user = User(email="test@example.com", password_hash=hash_password("12345678"), full_name="Test")
    db.add(user)
    db.commit()
    return user


def test_hash_password():
    hashed = hash_password("12345678")
    assert hashed != "12345678"
    assert verify_password("12345678", hashed)
    assert not verify_password("otra-clave", hashed)


def test_jwt_token():
    token, _ = create_access_token(1)
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert "exp" in payload


def test_otp_has_6_digits():
    code = otp_service.generate_code()
    assert len(code) == 6
    assert code.isdigit()


def test_otp_single_use(db):
    user = create_user(db)
    code = otp_service.create_otp(db, user.id)
    assert otp_service.verify_otp(db, user.id, code) is True
    assert otp_service.verify_otp(db, user.id, code) is False


def test_otp_expired(db):
    user = create_user(db)
    code = otp_service.create_otp(db, user.id)
    otp = db.query(OTPCode).first()
    otp.expires_at = datetime.utcnow() - timedelta(minutes=1)
    db.commit()
    assert otp_service.verify_otp(db, user.id, code) is False

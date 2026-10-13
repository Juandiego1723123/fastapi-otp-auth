"""Endpoints de autenticación."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, limiter
from app.models import LoginSession, User
from app.schemas import Message, OTPResend, OTPVerify, Token, UserLogin, UserOut, UserRegister
from app.services import email_service, otp_service
from app.services.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger(__name__)


def send_code(db: Session, user: User):
    """Genera un OTP y lo envía por correo. Responde 503 si el correo falla."""
    code = otp_service.create_otp(db, user.id)
    try:
        email_service.send_otp_email(user.email, code)
    except Exception:
        logger.error("Error enviando correo OTP")
        raise HTTPException(status_code=503, detail="No se pudo enviar el correo")


def new_session(db: Session, user_id: int) -> Token:
    """Crea un JWT y lo guarda en login_sessions."""
    token, expires_at = create_access_token(user_id)
    db.add(LoginSession(user_id=user_id, token=token, expires_at=expires_at))
    db.commit()
    return Token(access_token=token)


@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit("10/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    """Registra un usuario con la contraseña hasheada."""
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    user = User(email=data.email, password_hash=hash_password(data.password), full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Message)
@limiter.limit("5/minute")
def login(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    """Valida credenciales y envía un OTP al correo. No devuelve token."""
    user = db.query(User).filter(User.email == data.email).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    send_code(db, user)
    return Message(message="Código enviado al correo")


@router.post("/verify-otp", response_model=Token)
@limiter.limit("10/minute")
def verify_otp(request: Request, data: OTPVerify, db: Session = Depends(get_db)):
    """Verifica el OTP y entrega el JWT."""
    user = db.query(User).filter(User.email == data.email).first()
    if user is None or not otp_service.verify_otp(db, user.id, data.code):
        raise HTTPException(status_code=400, detail="Código inválido o expirado")

    return new_session(db, user.id)


@router.post("/resend-otp", response_model=Message)
@limiter.limit("3/minute")
def resend_otp(request: Request, data: OTPResend, db: Session = Depends(get_db)):
    """Envía un nuevo OTP e invalida el anterior."""
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    send_code(db, user)
    return Message(message="Nuevo código enviado al correo")


@router.post("/refresh", response_model=Token)
def refresh(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Revoca el token actual y entrega uno nuevo."""
    db.query(LoginSession).filter(LoginSession.token == request.state.token).update({"revoked": True})
    db.commit()
    return new_session(db, user.id)


@router.post("/logout", response_model=Message)
def logout(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Cierra la sesión revocando el token."""
    db.query(LoginSession).filter(LoginSession.token == request.state.token).update({"revoked": True})
    db.commit()
    return Message(message="Sesión cerrada")

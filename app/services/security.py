"""Hash de contraseñas con bcrypt y manejo de tokens JWT."""

import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    """Devuelve el hash bcrypt de la contraseña."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Compara la contraseña con su hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: int):
    """Crea un JWT con el id del usuario y su fecha de expiración."""
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # jti hace que cada token sea único aunque se creen en el mismo segundo
    payload = {"sub": str(user_id), "exp": expires_at, "iat": datetime.utcnow(), "jti": uuid.uuid4().hex}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expires_at


def decode_access_token(token: str) -> dict:
    """Verifica firma y expiración del token. Lanza excepción si no es válido."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

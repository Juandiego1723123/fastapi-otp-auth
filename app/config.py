"""Configuración leída desde variables de entorno (.env)."""

import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-esta-clave-en-produccion-1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

OTP_EXPIRE_MINUTES = 15

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Si es true, el OTP se imprime en consola en vez de enviarse (solo para pruebas locales)
EMAIL_DEV_MODE = os.getenv("EMAIL_DEV_MODE", "false").lower() == "true"

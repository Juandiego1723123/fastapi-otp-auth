"""Aplicación principal de FastAPI."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import Base, engine
from app.dependencies import limiter
from app.middleware import AuthMiddleware
from app.routes import auth, users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Autenticación con OTP")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(users.router)


@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    """Responde un error genérico sin mostrar detalles internos."""
    logger.exception("Error interno")
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


@app.get("/")
def root():
    """Verifica que la API está funcionando."""
    return {"status": "ok"}

"""Middleware que protege las rutas que requieren token."""

import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app import database
from app.models import LoginSession
from app.services.security import decode_access_token

PROTECTED_ROUTES = ["/users", "/auth/refresh", "/auth/logout"]


class AuthMiddleware(BaseHTTPMiddleware):
    """Valida el JWT y que la sesión no esté revocada antes de llegar al endpoint."""

    async def dispatch(self, request, call_next):
        path = request.url.path
        if not any(path.startswith(route) for route in PROTECTED_ROUTES):
            return await call_next(request)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Token requerido"})
        token = auth.split(" ")[1]

        try:
            payload = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expirado"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Token inválido"})

        db = database.SessionLocal()
        try:
            session = db.query(LoginSession).filter(LoginSession.token == token).first()
            if session is None or session.revoked:
                return JSONResponse(status_code=401, content={"detail": "Sesión cerrada"})
        finally:
            db.close()

        request.state.user_id = int(payload["sub"])
        request.state.token = token
        return await call_next(request)

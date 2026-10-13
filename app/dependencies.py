"""Dependencias compartidas: rate limiter y usuario autenticado."""

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

limiter = Limiter(key_func=get_remote_address)

# Muestra el botón "Authorize" en /docs. La validación la hace el middleware.
bearer = HTTPBearer(auto_error=False)


def get_current_user(request: Request, db: Session = Depends(get_db), _=Depends(bearer)) -> User:
    """Devuelve el usuario que el middleware ya autenticó."""
    user = db.get(User, request.state.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

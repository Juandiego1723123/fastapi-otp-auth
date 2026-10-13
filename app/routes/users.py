"""Endpoints del perfil de usuario (requieren token)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserOut)
def get_profile(user: User = Depends(get_current_user)):
    """Devuelve el perfil del usuario autenticado."""
    return user


@router.put("/profile", response_model=UserOut)
def update_profile(data: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Actualiza el nombre del usuario autenticado."""
    user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user

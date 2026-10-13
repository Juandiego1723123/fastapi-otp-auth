"""Conexión a la base de datos SQLite con SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """Abre una sesión de base de datos por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

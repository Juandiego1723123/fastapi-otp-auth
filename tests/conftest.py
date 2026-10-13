import os
import tempfile

# Base de datos temporal solo para los tests
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(tempfile.mkdtemp(), "test.db")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.dependencies import limiter  # noqa: E402
from app.main import app  # noqa: E402
from app.services import email_service  # noqa: E402

limiter.enabled = False


@pytest.fixture(autouse=True)
def clean_db():
    """Reinicia las tablas antes de cada test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def emails(monkeypatch):
    """Reemplaza el envío real de correo y guarda los códigos enviados."""
    sent = []
    monkeypatch.setattr(email_service, "send_otp_email", lambda to, code: sent.append(code))
    return sent


@pytest.fixture
def client(emails):
    return TestClient(app)

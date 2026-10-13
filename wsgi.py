"""Punto de entrada WSGI para desplegar en PythonAnywhere."""

import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))

from a2wsgi import ASGIMiddleware  # noqa: E402

from app.main import app  # noqa: E402

_wsgi_app = None


def application(environ, start_response):
    """Adapta FastAPI (ASGI) a WSGI. Se crea en la primera peticion, dentro del proceso trabajador."""
    global _wsgi_app
    if _wsgi_app is None:
        _wsgi_app = ASGIMiddleware(app)
    return _wsgi_app(environ, start_response)

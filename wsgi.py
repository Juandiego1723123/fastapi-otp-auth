"""Punto de entrada WSGI para desplegar en PythonAnywhere."""

import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))

from a2wsgi import ASGIMiddleware  # noqa: E402

from app.main import app  # noqa: E402

# PythonAnywhere usa WSGI; a2wsgi adapta la app ASGI de FastAPI
application = ASGIMiddleware(app)

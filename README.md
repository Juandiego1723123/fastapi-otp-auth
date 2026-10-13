# Sistema de Autenticación con OTP - FastAPI

API de autenticación con doble factor: el usuario inicia sesión con correo y contraseña, recibe un código OTP de 6 dígitos en su correo (válido 15 minutos) y con ese código obtiene un token JWT.

**Tecnologías:** FastAPI, SQLAlchemy, SQLite, PyOTP, bcrypt, PyJWT, smtplib, slowapi, pytest.

## Endpoints

| Método | Ruta | Descripción | Requiere token |
|---|---|---|---|
| POST | /auth/register | Registrar usuario | No |
| POST | /auth/login | Login y envío de OTP | No |
| POST | /auth/verify-otp | Verificar OTP y obtener token | No |
| POST | /auth/resend-otp | Reenviar OTP | No |
| POST | /auth/refresh | Obtener un token nuevo | Sí |
| POST | /auth/logout | Cerrar sesión | Sí |
| GET | /users/profile | Ver perfil | Sí |
| PUT | /users/profile | Actualizar perfil | Sí |

## Estructura

```
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── middleware.py
├── dependencies.py
├── routes/
│   ├── auth.py
│   └── users.py
└── services/
    ├── email_service.py
    ├── otp_service.py
    └── security.py
tests/
├── test_unit.py
└── test_integration.py
```

## Seguridad

- Contraseñas guardadas con bcrypt.
- JWT con expiración.
- OTP de un solo uso que vence a los 15 minutos.
- Middleware que valida el token y que la sesión no esté revocada.
- Logout revoca el token en la tabla `login_sessions`.
- Rate limiting en login, registro y OTP.
- Los errores internos no muestran detalles al usuario.

## Instalación

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # luego completar los datos
uvicorn app.main:app --reload
```

Documentación: http://127.0.0.1:8000/docs

Para enviar correos con Gmail se necesita una contraseña de aplicación en `SMTP_PASSWORD` y `EMAIL_DEV_MODE=false`.

## Tests

```bash
pytest
```

5 tests unitarios y 3 de integración.

## Despliegue

Desplegado en **PythonAnywhere** (plan gratuito, permite SMTP con Gmail).

- `wsgi.py` adapta la app ASGI de FastAPI a WSGI con `a2wsgi`, que es el formato que usa PythonAnywhere.
- Las variables de entorno se configuran en el archivo `.env` del servidor.
- Para correr en local se usa Uvicorn: `uvicorn app.main:app --reload`.

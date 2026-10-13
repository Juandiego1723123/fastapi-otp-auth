"""Tests de integración de los endpoints."""

USER = {"email": "juan@example.com", "password": "12345678", "full_name": "Juan"}


def login_completo(client, emails):
    """Registra, hace login y verifica el OTP. Devuelve el token."""
    client.post("/auth/register", json=USER)
    client.post("/auth/login", json={"email": USER["email"], "password": USER["password"]})
    response = client.post("/auth/verify-otp", json={"email": USER["email"], "code": emails[-1]})
    return response.json()["access_token"]


def test_flujo_completo(client, emails):
    token = login_completo(client, emails)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/profile", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == USER["email"]

    response = client.put("/users/profile", headers=headers, json={"full_name": "Juan Diego"})
    assert response.json()["full_name"] == "Juan Diego"

    assert client.post("/auth/logout", headers=headers).status_code == 200
    # Después del logout el token ya no sirve
    assert client.get("/users/profile", headers=headers).status_code == 401


def test_login_incorrecto_y_otp_invalido(client, emails):
    client.post("/auth/register", json=USER)
    assert client.post("/auth/register", json=USER).status_code == 409

    response = client.post("/auth/login", json={"email": USER["email"], "password": "incorrecta"})
    assert response.status_code == 401

    client.post("/auth/login", json={"email": USER["email"], "password": USER["password"]})
    response = client.post("/auth/verify-otp", json={"email": USER["email"], "code": "000000"})
    assert response.status_code == 400


def test_rutas_protegidas_sin_token(client):
    assert client.get("/users/profile").status_code == 401
    assert client.post("/auth/logout").status_code == 401
    headers = {"Authorization": "Bearer token-falso"}
    assert client.get("/users/profile", headers=headers).status_code == 401

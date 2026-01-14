"""Testes de autenticação JWT."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt
from utils.settings import settings


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_login_success(mock_auth, client):
    """Testa login bem-sucedido retornando JWT."""
    mock_auth.return_value = "admin"
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "valid_token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    mock_auth.assert_called_once_with("valid_token")


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_login_failure_invalid_token(mock_auth, client):
    """Testa login com token inválido."""
    mock_auth.side_effect = ValueError("Token inválido")
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "invalid_token"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Credenciais inválidas"


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_login_failure_wrong_user(mock_auth, client):
    """Testa login com token que pertence a outro usuário."""
    mock_auth.return_value = "outro_usuario"
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "token_de_outro"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Token não pertence a este usuário"


def test_get_current_user(authenticated_client, mock_username):
    """Testa endpoint /me com usuário autenticado."""
    response = authenticated_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data == {"username": "test_user", "status": "authenticated via JWT"}


def test_get_current_user_unauthorized(client):
    """Testa endpoint /me sem autenticação."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_current_user_expired_token(client):
    """Testa endpoint /me com token JWT expirado."""
    expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)
    to_encode = {
        "sub": "test_user",
        "exp": expired_time,
        "nbf": datetime.now(timezone.utc) - timedelta(minutes=5),
        "iat": datetime.now(timezone.utc) - timedelta(minutes=5),
        "iss": "NewsGrid-Backend",
    }
    expired_token = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_get_current_user_invalid_signature(client):
    """Testa endpoint /me com token JWT com assinatura inválida."""
    current_time = datetime.now(timezone.utc)
    to_encode = {
        "sub": "test_user",
        "exp": current_time + timedelta(minutes=30),
        "nbf": current_time,
        "iat": current_time,
        "iss": "NewsGrid-Backend",
    }
    invalid_token = jwt.encode(
        to_encode,
        "wrong_secret_key",
        algorithm=settings.jwt_algorithm,
    )
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_get_current_user_malformed_token(client):
    """Testa endpoint /me com token JWT malformado."""
    headers = {"Authorization": "Bearer malformed.jwt.token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

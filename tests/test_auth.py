"""Testes de autenticação JWT."""

from datetime import UTC, datetime, timedelta
from unittest.mock import ANY, Mock, patch

import jwt

from utils.settings import settings


@patch("app.api.auth.controller.AuthServiceSQL.get_user_by_username")
@patch("app.api.auth.controller.AuthServiceSQL.verify_password")
def test_login_success(mock_verify, mock_get, client):
    """Testa login bem-sucedido retornando JWT."""
    mock_user = Mock()
    mock_user.id = 1
    mock_user.username = "admin"
    mock_get.return_value = mock_user
    mock_verify.return_value = True
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "valid_token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    mock_get.assert_called_once_with(ANY, "admin")
    mock_verify.assert_called_once()


@patch("app.api.auth.controller.AuthServiceSQL.get_user_by_username")
def test_login_failure_invalid_token(mock_get, client):
    """Testa login com token inválido."""
    mock_get.return_value = None
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "invalid"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciais inválidas"


@patch("app.api.auth.controller.AuthServiceSQL.get_user_by_username")
@patch("app.api.auth.controller.AuthServiceSQL.verify_password")
def test_login_failure_wrong_user(mock_verify, mock_get, client):
    """Testa login com usuário errado."""
    mock_user = Mock()
    mock_user.id = 1
    mock_get.return_value = mock_user
    mock_verify.return_value = False
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciais inválidas"


def test_get_current_user(authenticated_client):
    """Testa endpoint /me com usuário autenticado."""
    response = authenticated_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data == {"username": "testuser", "status": "authenticated via JWT"}


def test_get_current_user_unauthorized(client):
    """Testa endpoint /me sem autenticação."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_current_user_expired_token(client):
    """Testa endpoint /me com token JWT expirado."""
    expired_time = datetime.now(UTC) - timedelta(minutes=1)
    to_encode = {
        "sub": "test_user",
        "exp": expired_time,
        "nbf": datetime.now(UTC) - timedelta(minutes=5),
        "iat": datetime.now(UTC) - timedelta(minutes=5),
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
    current_time = datetime.now(UTC)
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

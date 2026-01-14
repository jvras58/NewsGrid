"""Testes de autenticação JWT."""

from unittest.mock import patch


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

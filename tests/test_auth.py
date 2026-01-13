from unittest.mock import patch


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
@patch("app.api.auth.controller.AuthService.create_session")
def test_login_success(mock_create_session, mock_auth, client):
    mock_auth.return_value = "admin"
    mock_create_session.return_value = "session123"
    response = client.post("/api/v1/auth/login", json={"token": "valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Login realizado", "user": "admin"}
    mock_auth.assert_called_once_with("valid_token")
    mock_create_session.assert_called_once_with("admin")


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_login_failure(mock_auth, client):
    mock_auth.side_effect = ValueError("Token inválido")
    response = client.post("/api/v1/auth/login", json={"token": "invalid_token"})
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Token inválido"


@patch("app.api.auth.controller.AuthService.delete_session")
def test_logout(mock_delete_session, client):
    client.cookies.set("session_id", "session123")
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Logout realizado"}
    mock_delete_session.assert_called_once_with("session123")


def test_get_current_user(client, mock_username):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data == {"username": "test_user", "status": "authenticated"}

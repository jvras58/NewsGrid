from unittest.mock import patch


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
@patch("app.api.auth.controller.AuthService.create_session")
def test_login_success(mock_create_session, mock_auth, authenticated_client):
    mock_auth.return_value = "admin"
    mock_create_session.return_value = "session123"
    response = authenticated_client.post(
        "/api/v1/auth/login", json={"token": "valid_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Login realizado", "user": "admin"}
    mock_auth.assert_called_once_with("valid_token")
    mock_create_session.assert_called_once_with("admin")


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_login_failure(mock_auth, authenticated_client):
    mock_auth.side_effect = ValueError("Token inválido")
    response = authenticated_client.post(
        "/api/v1/auth/login", json={"token": "invalid_token"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Token inválido"


@patch("app.api.auth.controller.AuthService.delete_session")
def test_logout(mock_delete_session, authenticated_client):
    authenticated_client.cookies.set("session_id", "session123")
    response = authenticated_client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Logout realizado"}
    mock_delete_session.assert_called_once_with("session123")


def test_get_current_user(authenticated_client, mock_username):
    response = authenticated_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data == {"username": "test_user", "status": "authenticated"}


# ============ Testes para fluxo híbrido (Cookie + Bearer Token) ============


@patch("app.api.auth.controller.AuthService.get_user_by_session")
def test_get_current_user_via_cookie(mock_get_session, client):
    """
    Testa get_current_user com autenticação via cookie.
    Justificativa: Validar que navegadores podem autenticar com session_id cookie.
    """
    mock_get_session.return_value = "cookie_user"

    # Simula requisição com cookie
    client.cookies.set("session_id", "valid_session_123")
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "cookie_user"
    assert data["status"] == "authenticated"
    mock_get_session.assert_called_once_with("valid_session_123")


@patch("app.services.auth_service.AuthService.authenticate_by_token")
def test_get_current_user_via_bearer_token(mock_auth_token, client):
    """
    Testa get_current_user com autenticação via Bearer token.
    Justificativa: Validar que APIs/scripts podem autenticar com Bearer token no header.
    """
    mock_auth_token.return_value = "bearer_user"

    # Simula requisição com Bearer token
    headers = {"Authorization": "Bearer valid_token_123"}
    response = client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "bearer_user"
    assert data["status"] == "authenticated"
    mock_auth_token.assert_called_once_with("valid_token_123")


@patch("app.api.auth.controller.AuthService.get_user_by_session")
@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_get_current_user_prefers_cookie_over_token(
    mock_auth_token, mock_get_session, client
):
    """
    Testa que get_current_user prioriza cookie sobre Bearer token.
    Justificativa: Garantir que se ambos estiverem presentes, cookie tem precedência.
    """
    mock_get_session.return_value = "cookie_user"
    mock_auth_token.return_value = "bearer_user"

    # Simula requisição com AMBOS cookie e Bearer token
    client.cookies.set("session_id", "valid_session_123")
    headers = {"Authorization": "Bearer valid_token_123"}
    response = client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    # Deve retornar o usuário do cookie, não do token
    assert data["username"] == "cookie_user"
    mock_get_session.assert_called_once()
    # authenticate_by_token não deve ser chamado pois cookie foi bem-sucedido
    mock_auth_token.assert_not_called()


def test_get_current_user_no_auth_fails(client):
    """
    Testa que get_current_user falha sem cookie ou Bearer token.
    Justificativa: Validar que requisições sem autenticação são rejeitadas.
    """
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Não autenticado" in data["detail"]


@patch("app.api.auth.controller.AuthService.authenticate_by_token")
def test_get_current_user_invalid_bearer_token_fails(mock_auth_token, client):
    """
    Testa que get_current_user falha com Bearer token inválido.
    Justificativa: Garantir que tokens malformados/inválidos são rejeitados.
    """
    mock_auth_token.side_effect = ValueError("Token inválido")

    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

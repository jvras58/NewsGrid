from unittest.mock import patch


@patch("app.api.user.controller.AuthService.create_user")
def test_create_user_success(mock_create, client):
    mock_create.return_value = {
        "username": "newuser",
        "token": "token123",
        "status": "created",
    }
    response = client.post(
        "/api/v1/users/", json={"username": "newuser", "token": "token123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"username": "newuser", "token": "token123", "status": "created"}
    mock_create.assert_called_once_with("newuser", "token123")


@patch("app.api.user.controller.AuthService.create_user")
def test_create_user_failure(mock_create, client):
    mock_create.side_effect = ValueError("Usuário já existe")
    response = client.post(
        "/api/v1/users/", json={"username": "existing", "token": "token123"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Usuário já existe"


@patch("app.api.user.controller.AuthService.list_users")
def test_list_users(mock_list, client):
    mock_list.return_value = ["admin", "user1"]
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert data == ["admin", "user1"]
    mock_list.assert_called_once()


@patch("app.api.user.controller.AuthService.revoke_user")
def test_revoke_user_success(
    mock_revoke,
    client,
):
    mock_revoke.return_value = {"status": "revoked", "username": "user1"}
    response = client.delete("/api/v1/users/user1")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "revoked", "username": "user1"}
    mock_revoke.assert_called_once_with("user1")


@patch("app.api.user.controller.AuthService.revoke_user")
def test_revoke_user_not_found(
    mock_revoke,
    client,
):
    mock_revoke.side_effect = ValueError("Usuário não encontrado")
    response = client.delete("/api/v1/users/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Usuário não encontrado"

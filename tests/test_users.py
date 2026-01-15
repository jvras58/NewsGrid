from unittest.mock import patch


@patch("app.api.user.controller.AuthServiceSQL.create_user")
def test_create_user_success(mock_create, authenticated_client):
    mock_create.return_value = {"user_id": 123}
    response = authenticated_client.post(
        "/api/v1/users/",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "username": "newuser",
        "email": "new@example.com",
        "status": "created",
    }
    mock_create.assert_called_once()


@patch("app.api.user.controller.AuthServiceSQL.create_user")
def test_create_user_failure(mock_create, authenticated_client):
    mock_create.side_effect = ValueError("Usuário já existe")
    response = authenticated_client.post(
        "/api/v1/users/",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Usuário já existe"


@patch("app.api.user.controller.AuthServiceSQL.list_usernames")
def test_list_users(mock_list, authenticated_client):
    mock_list.return_value = ["user1", "user2"]
    response = authenticated_client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert data == ["user1", "user2"]
    mock_list.assert_called_once()

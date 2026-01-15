# from unittest.mock import Mock, patch
# from uuid import UUID


# @patch("app.api.user.controller.AuthServiceSQL.create_user")
# def test_create_user_success(mock_create, authenticated_client):
#     mock_create.return_value = None
#     response = authenticated_client.post(
#         "/api/v1/users/",
#         json={
#             "username": "newuser",
#             "email": "new@example.com",
#             "password": "password123",
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {
#         "username": "newuser",
#         "email": "new@example.com",
#         "status": "created",
#     }
#     mock_create.assert_called_once()


# @patch("app.api.user.controller.AuthServiceSQL.create_user")
# def test_create_user_failure(mock_create, authenticated_client):
#     mock_create.side_effect = ValueError("Usuário já existe")
#     response = authenticated_client.post(
#         "/api/v1/users/",
#         json={
#             "username": "newuser",
#             "email": "new@example.com",
#             "password": "password123",
#         },
#     )
#     assert response.status_code == 400
#     data = response.json()
#     assert data["detail"] == "Usuário já existe"


# @patch("app.api.user.controller.AuthServiceSQL.list_usernames")
# def test_list_users(mock_list, authenticated_client):
#     mock_list.return_value = ["user1", "user2"]
#     response = authenticated_client.get("/api/v1/users/")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == ["user1", "user2"]
#     mock_list.assert_called_once()
#     data = response.json()
#     assert data == ["admin", "user1"]
#     mock_list.assert_called_once()


# @patch("app.api.user.controller.AuthService.revoke_user")
# def test_revoke_user_success(
#     mock_revoke,
#     authenticated_client,
# ):
#     mock_revoke.return_value = {"status": "revoked", "username": "user1"}
#     response = authenticated_client.delete("/api/v1/users/user1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {"status": "revoked", "username": "user1"}
#     mock_revoke.assert_called_once_with("user1")


# @patch("app.api.user.controller.AuthService.revoke_user")
# def test_revoke_user_not_found(
#     mock_revoke,
#     authenticated_client,
# ):
#     mock_revoke.side_effect = ValueError("Usuário não encontrado")
#     response = authenticated_client.delete("/api/v1/users/nonexistent")
#     assert response.status_code == 404
#     data = response.json()
#     assert "detail" in data
#     assert data["detail"] == "Usuário não encontrado"

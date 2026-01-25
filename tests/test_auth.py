from unittest.mock import patch

from fastapi.testclient import TestClient

from app.startup import app

client = TestClient(app)


# def test_login_success(container):
#     with patch.object(container.login_use_case(), "execute", return_value="fake_token"):
#         response = client.post(
#             "/api/v1/auth/login", data={"username": "admin", "password": "admin123"}
#         )
#         assert response.status_code == 200
#         assert "access_token" in response.json()


def test_login_failure(container):
    with patch.object(
        container.login_use_case(),
        "execute",
        side_effect=Exception("Credenciais inválidas"),
    ):
        response = client.post(
            "/api/v1/auth/login", data={"username": "invalid", "password": "wrong"}
        )
        assert response.status_code == 401

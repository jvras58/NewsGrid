import pytest
from fastapi.testclient import TestClient

from app.api.auth.controller import get_current_user
from app.models import User
from app.startup import app


# TODO: TODOS OS TESTES PRECISAM SER REFEITOS PARA USAR O SERVICO COM BANCO DE DADOS POSTGRESQL
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def authenticated_client():
    mock_user = User(
        id=1, username="testuser", email="test@example.com", hashed_password="hashed"
    )
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield TestClient(app)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_username():
    return 1


@pytest.fixture
def mock_token():
    return "test_token"

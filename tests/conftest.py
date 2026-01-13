import pytest
from fastapi.testclient import TestClient
from app.startup import app
from app.api.auth.controller import get_current_user


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def authenticated_client():
    """Cliente com override para get_current_user."""

    def mock_get_current_user():
        return "test_user"

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield TestClient(app)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_username():
    return "test_user"


@pytest.fixture
def mock_token():
    return "test_token"

import pytest
from fastapi.testclient import TestClient

from app.api.auth.controller import get_current_user
from app.startup import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def authenticated_client():
    app.dependency_overrides[get_current_user] = lambda: "test_user"
    yield TestClient(app)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_username():
    return "test_user"


@pytest.fixture
def mock_token():
    return "test_token"

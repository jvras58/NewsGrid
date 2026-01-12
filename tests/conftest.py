import pytest
from fastapi.testclient import TestClient
from app.startup import app
from app.api.auth.controller import verify_token


@pytest.fixture
def client():
    app.dependency_overrides[verify_token] = lambda: "test_user"
    return TestClient(app)


@pytest.fixture
def mock_username():
    return "test_user"


@pytest.fixture
def mock_token():
    return "test_token"

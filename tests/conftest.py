import pytest
from fastapi.testclient import TestClient
from app.startup import app


@pytest.fixture
def client():
    return TestClient(app)


import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function")
def test_client():
    """Create a test client for testing fastapi"""

    with TestClient(app) as test_client:
        yield test_client


from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_returns_welcome_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_is_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
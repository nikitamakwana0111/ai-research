from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_research_route_validation_error():
    response = client.post("/api/v1/research/start", json={"topic": ""})
    assert response.status_code == 422

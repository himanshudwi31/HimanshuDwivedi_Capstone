from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)

def test_ask_rejects_missing_question():
    response = client.post("/ask", json={})
    assert response.status_code == 422
    body = response.json()
    print(body)
    detail_text = str(body.get("detail", ""))
    assert "question" in detail_text.lower()


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
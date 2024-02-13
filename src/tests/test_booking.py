from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_is_available():
    data = {
        "publication_id": "c7edea7e-7d60-4506-9166-736ff196062f",
        "date": "2024-10-02",
        "participant": 1
    }
    response = client.post("/api/booking/availability", json=data)
    assert response.status_code == 200
    assert response.json() == True


def test_not_available():
    data = {
        "publication_id": "682bb453-0432-47a0-8098-01d90b5740ec",
        "date": "2024-10-02",
        "participant": 2
    }
    response = client.post("/api/booking/availability", json=data)
    assert response.status_code == 200
    assert response.json() == False

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_is_available():
    data = {
        "publication_id": "2181b7f1-835f-4758-86ec-12a0505852be",
        "date": "2024-10-02",
        "participant": 1
    }
    response = client.post("/api/booking/availability", json=data)
    assert response.status_code == 200
    assert response.json() == True


def test_not_available():
    data = {
        "publication_id": "2181b7f1-835f-4758-86ec-12a0505852be",
        "date": "2024-10-02",
        "participant": 2
    }
    response = client.post("/api/booking/availability", json=data)
    assert response.status_code == 200
    assert response.json() == False

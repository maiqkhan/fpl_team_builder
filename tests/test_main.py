from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root_unathorized():
    response = client.get("/")
    assert response.status_code == 200
    assert response.cookies == {}

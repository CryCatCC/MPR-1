from fastapi.testclient import TestClient
from auth_service.main import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == 6
    assert data["token"] == "valid-token-601"


def test_validate_token():
    response = client.get(
        "/validate-token",
        params={"token": "valid-token-601"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == 6
    assert data["valid"] is True

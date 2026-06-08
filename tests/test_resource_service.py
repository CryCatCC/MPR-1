from fastapi.testclient import TestClient
from unittest.mock import patch

from resource_service.main import app

client = TestClient(app)


@patch("resource_service.main.validate_user_token")
def test_get_secure_data(mock_validate):

    mock_validate.return_value = {
        "valid": True
    }

    response = client.get(
        "/secure-data",
        params={"token": "valid-token-601"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == 6
    assert data["data"]["resource_id"] == 601


@patch("resource_service.main.validate_user_token")
def test_update_data(mock_validate):

    mock_validate.return_value = {
        "valid": True
    }

    response = client.post(
        "/update-data",
        json={
            "token": "valid-token-601",
            "new_content": "Updated content"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == 6

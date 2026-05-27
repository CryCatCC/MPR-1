from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

STUDENT_N = int(os.getenv("STUDENT_N", 6))

AUTH_SERVICE_URL = "http://auth-service-06:8000"

app = FastAPI(title=f"Resource API N{STUDENT_N}")

SECURE_DATA = {
    "resource_id": 601,
    "content": "Protected resource data"
}


class UpdateRequest(BaseModel):
    token: str
    new_content: str


def validate_user_token(token: str):

    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/validate-token",
            params={"token": token}
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Auth Service unavailable"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return response.json()


@app.get("/secure-data")
def get_secure_data(token: str):

    validate_user_token(token)

    return {
        "student_id": STUDENT_N,
        "data": SECURE_DATA
    }


@app.post("/update-data")
def update_data(request: UpdateRequest):

    validate_user_token(request.token)

    SECURE_DATA["content"] = request.new_content

    return {
        "student_id": STUDENT_N,
        "message": "Data updated successfully",
        "updated_data": SECURE_DATA
    }
    
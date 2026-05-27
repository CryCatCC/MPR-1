from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

STUDENT_N = int(os.getenv("STUDENT_N", 6))

app = FastAPI(title=f"Auth Service N{STUDENT_N}")

# Імітація користувачів
USERS = {
    "admin": "password123"
}

# Імітація токенів
TOKENS = {
    "valid-token-601": "admin"
}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: LoginRequest):

    if USERS.get(data.username) != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "student_id": STUDENT_N,
        "token": "valid-token-601",
        "message": "Authentication successful"
    }


@app.get("/validate-token")
def validate_token(token: str):

    if token not in TOKENS:
        raise HTTPException(status_code=403, detail="Invalid token")

    return {
        "student_id": STUDENT_N,
        "valid": True,
        "user": TOKENS[token]
    }

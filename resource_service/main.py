# FastAPI використовується для створення REST API сервісу
from fastapi import FastAPI, HTTPException

# BaseModel — для валідації JSON запитів (request body)
from pydantic import BaseModel

# requests — для HTTP запитів до іншого мікросервісу (Auth Service)
import requests

# os — для читання змінних середовища (Docker)
import os


# ---------------------------
# ПЕРСОНАЛІЗАЦІЯ СЕРВІСУ
# ---------------------------

# Номер студента береться з Docker environment
STUDENT_N = int(os.getenv("STUDENT_N", 6))


# URL іншого мікросервісу (Auth Service)
# ВАЖЛИВО: використовується ім’я сервісу з docker-compose, а не localhost
AUTH_SERVICE_URL = "http://auth_service:8000"


# Створення FastAPI застосунку
app = FastAPI(title=f"Resource API N{STUDENT_N}")


# ---------------------------
# ІМІТАЦІЯ ЗАХИЩЕНИХ ДАНИХ
# ---------------------------

# Це умовна "база даних", яку захищає сервіс
SECURE_DATA = {
    "resource_id": 601,
    "content": "Protected resource data"
}


# ---------------------------
# МОДЕЛЬ ДЛЯ ОНОВЛЕННЯ ДАНИХ
# ---------------------------

# Опис структури JSON для /update-data
class UpdateRequest(BaseModel):
    token: str        # токен доступу
    new_content: str  # новий текст, який оновлює ресурс


# ---------------------------
# ФУНКЦІЯ ВАЛІДАЦІЇ ТОКЕНА
# ---------------------------

def validate_user_token(token: str):

    try:
        # Запит до Auth Service для перевірки токена
        response = requests.get(
            f"{AUTH_SERVICE_URL}/validate-token",
            params={"token": token}   # передаємо token як query параметр
        )

    except requests.exceptions.ConnectionError:
        # Якщо Auth Service недоступний
        raise HTTPException(
            status_code=503,
            detail="Auth Service unavailable"
        )

    # Якщо Auth Service відхилив токен
    if response.status_code != 200:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Якщо токен валідний → повертаємо відповідь Auth Service
    return response.json()


# ---------------------------
# ENDPOINT: ОТРИМАННЯ ДАНИХ
# ---------------------------

@app.get("/secure-data")
def get_secure_data(token: str):

    # Перед доступом перевіряємо токен через Auth Service
    validate_user_token(token)

    # Якщо токен валідний → повертаємо дані
    return {
        "student_id": STUDENT_N,  # персоналізація
        "data": SECURE_DATA       # захищений ресурс
    }


# ---------------------------
# ENDPOINT: ОНОВЛЕННЯ ДАНИХ
# ---------------------------

@app.post("/update-data")
def update_data(request: UpdateRequest):

    # Перевірка доступу через токен
    validate_user_token(request.token)

    # Оновлення "бази даних" у пам’яті
    SECURE_DATA["content"] = request.new_content

    # Повернення результату операції
    return {
        "student_id": STUDENT_N,
        "message": "Data updated successfully",
        "updated_data": SECURE_DATA
    }

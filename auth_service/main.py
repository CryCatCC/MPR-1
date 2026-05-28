# Імпорт FastAPI для створення REST API сервісу
from fastapi import FastAPI, HTTPException

# BaseModel використовується для валідації вхідних JSON-даних (request body)
from pydantic import BaseModel

# Модуль os використовується для читання змінних середовища (Docker environment)
import os


# Отримання номера студента з environment (Docker-compose)
# Якщо змінна не задана — використовується значення 6 як default
STUDENT_N = int(os.getenv("STUDENT_N", 6))


# Створення FastAPI застосунку з назвою, яка включає номер студента
app = FastAPI(title=f"Auth Service N{STUDENT_N}")


# ---------------------------
# ІМІТАЦІЯ БАЗИ КОРИСТУВАЧІВ
# ---------------------------

# Словник користувачів: username -> password
USERS = {
    "admin": "password123"
}


# ---------------------------
# ІМІТАЦІЯ ТОКЕНІВ СЕСІЇ
# ---------------------------

# Словник токенів: token -> username
TOKENS = {
    "valid-token-601": "admin"
}


# ---------------------------
# МОДЕЛЬ ВХІДНИХ ДАНИХ LOGIN
# ---------------------------

# Pydantic модель, яка описує формат JSON для /login
class LoginRequest(BaseModel):
    username: str   # поле username у запиті
    password: str   # поле password у запиті


# ---------------------------
# ENDPOINT: LOGIN
# ---------------------------

@app.post("/login")
def login(data: LoginRequest):

    # Перевірка правильності логіну і пароля
    # USERS.get(...) повертає пароль по username або None
    if USERS.get(data.username) != data.password:
        # Якщо дані неправильні → повертаємо HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Якщо авторизація успішна → повертаємо відповідь
    return {
        "student_id": STUDENT_N,          # персоналізація сервісу
        "token": "valid-token-601",       # імітація JWT/сесійного токена
        "message": "Authentication successful"  # статус операції
    }


# ---------------------------
# ENDPOINT: VALIDATE TOKEN
# ---------------------------
# (цей endpoint використовується іншим мікросервісом)

@app.get("/validate-token")
def validate_token(token: str):

    # Перевірка: чи існує токен у словнику TOKENS
    if token not in TOKENS:
        # Якщо токен невалідний → заборона доступу
        raise HTTPException(status_code=403, detail="Invalid token")

    # Якщо токен валідний → повертаємо інформацію про нього
    return {
        "student_id": STUDENT_N,     # ідентифікатор студента
        "valid": True,                # підтвердження валідності токена
        "user": TOKENS[token]         # кому належить токен
    }

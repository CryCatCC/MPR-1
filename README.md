# MPR-Microservices Architecture "Security and Resources"

[![Automated API Tests](https://github.com/CryCatCC/MPR-/actions/workflows/api-tests.yml/badge.svg)](https://github.com/CryCatCC/MPR-/actions/workflows/api-tests.yml)

## 📌 Огляд проєкту

Цей проєкт демонструє практичну реалізацію **безпечної мікросервісної архітектури**.

### 🔹 Технологічний стек та ідеї:
* **Асинхронний фреймворк:** Обидва сервіси розроблені на базі FastAPI (Python 3.10).
* **Концепція Zero-Trust:** Наявність механізму внутрішньої HTTP-валідації маркерів (токенів) між сервісами.
* **Повна ізоляція:** Контейнеризація кожного компонента за допомогою окремих Dockerfile.
* **Декларативна оркестрація:** Одночасне розгортання та керування локальною мережею через Docker Compose.
* **Автоматизований контроль:** CI/CD конвеєр для безперервної інтеграції та контрактного тестування API.

---

## 🏗️ Архітектура взаємодії (Architecture)

```text
        ┌────────────────────────┐
        │      Resource API      │
        │      (порт: 9006)      │
        └───────────┬────────────┘
                    │ 
                    │ HTTP (Внутрішній запит)
                    │ GET /validate-token
                    ▼
        ┌────────────────────────┐
        │      Auth Service      │
        │      (порт: 8006)      │
        └────────────────────────┘
```

---

## 📁 Project Structure

```bash
microservices_project/
├── .github/workflows/
│   └── api-tests.yml        # Автоматичне тестування контрактів (Newman)
├── auth_service/            # Мікросервіс безпеки та автентифікації
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── resource_service/        # Мікросервіс захищених ресурсів
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── collection.json          # Експортований сценарій тестів Postman
└── docker-compose.yml       # Конфігурація оркестрації сервісів
```

---

## Services & Endpoints

### 🔑 Auth Service ( :8006 )

Method	Endpoint	      Description
POST	 /login	              Генерація сесійного токена
GET	 /validate-token	Внутрішня перевірка прав доступу маркеру

---
### 📦 Resource API ( :9006 )

Method	Endpoint	     Description
GET	 /secure-data	   Отримання захищених даних (потребує валідації)
POST	 /update-data	   Запис змін у систему (потребує валідації)

---
⚠️ Увага: Кожна JSON-відповідь обох серверів містить обов'язкове поле метаданих "student_id": 6

---

## 🧪 Testing

Тестування контрактів та працездатності API виконується за допомогою Postman Collection та консольного ранера Newman.

### 🔹 Запуск інтеграційних тестів локально:

```bash
# Встановлення консольної утиліти Newman
npm install -g newman

# Прогін тестувальних сценаріїв
newman run collection.json
```
---

## 🚀 Getting Started

### 🔧 Передумови:
Інстальований Docker
Інстальований Docker Compose

### ▶️ Локальний запуск системи:

```bash
# Збирання образів та запуск контейнерів у фоновому режимі
docker compose up -d --build

```

Після успішного старту точки доступу розгортаються за адресами:

🔑 Auth Service → http://localhost:8006

🗃️ Resource API → http://localhost:9006

---

## 🔄 CI/CD Конвеєр

Проєкт використовує технологію GitHub Actions для автоматичного забезпечення якості на кожному етапі розробки:

Автоматичний лінтинг коду на відповідність стандартам PEP8 за допомогою flake8.

Автоматичне підняття контейнерів у віртуальному ранері та перевірка API контракту через newman run.

---

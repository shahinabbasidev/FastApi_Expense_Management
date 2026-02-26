# Expense Management API

Modern **RESTful API** for tracking, categorizing, analyzing and managing personal or team expenses.

Clean architecture • Secure • Well-documented • Easy to extend

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub repo size](https://img.shields.io/github/repo-size/shahinabbasidev/Design_API_Expense_Management)
![GitHub last commit](https://img.shields.io/github/last-commit/shahinabbasidev/Design_API_Expense_Management)

## ✨ Features

- **User authentication & authorization** (JWT / OAuth2 planned)
- CRUD operations for **Expenses**, **Categories**, **Wallets/Accounts**
- Filter & search expenses (by date, category, amount, tags…)
- Monthly / yearly **summary statistics** and reports
- **Category-based** spending analytics
- Support for **multiple currencies** (planned / partial)
- Export data to **CSV / PDF** (planned)
- Input **validation** & proper **error handling**
- **OpenAPI / Swagger** documentation out-of-the-box

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL / SQLite (development)
- **ORM**: SQLAlchemy (most probable) or Tortoise-ORM
- **Authentication**: JWT (PyJWT / python-jose)
- **Validation**: Pydantic
- **Documentation**: Swagger UI + ReDoc (auto-generated)
- **Testing**: pytest
- **Other**: python-dotenv, alembic (migrations), loguru / structlog

## 🚀 Quick Start

### 📦 Sentry error tracking

This project includes optional Sentry integration for error monitoring and
performance tracing. The SDK is only activated when the `SENTRY_DSN` setting is
provided (you can put it in your `.env`). Example:

```
SENTRY_DSN=https://<public_key>@o0.ingest.sentry.io/12345
```

On startup the application will initialize the SDK with the FastAPI
integration and a low default `traces_sample_rate`. A helper endpoint
`GET /sentry-debug` triggers a division-by-zero error; use it to verify that
exceptions are being captured while running against a real project.

Feel free to adjust the DSN and sampling settings in `core/main.py`.

### 1. Clone the repository

```bash
git clone https://github.com/shahinabbasidev/Design_API_Expense_Management.git
cd Design_API_Expense_Management
# copy the example environment file and edit to your setup
cp .env.example .env

# using uv (recommended 2025+)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# or classic way
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Method,Endpoint,Description,Auth
POST,/auth/register,Register new user,—
POST,/auth/login,Login & get JWT,—
GET,/users/me,Get current user profile,JWT
POST,/expenses/,Create new expense,JWT
GET,/expenses/,List expenses (with filters),JWT
GET,/expenses/{id},Get single expense,JWT
PUT,/expenses/{id},Update expense,JWT
DELETE,/expenses/{id},Delete expense,JWT
GET,/expenses/summary,Monthly/yearly summary stats,JWT
GET,/categories/,List all categories,JWT


Method,Path,Description,Auth required
POST,/auth/register,Create new user,No
POST,/auth/login,Login → receive JWT token,No
GET,/users/me,Get current authenticated user,Yes
POST,/expenses/,Create new expense,Yes
GET,/expenses/,List all user expenses,Yes
GET,/expenses/{expense_id},Get one expense by ID,Yes
PUT,/expenses/{expense_id},Update expense,Yes
DELETE,/expenses/{expense_id},Delete expense,Yes
GET,/categories/,List available categories,Yes (maybe)
```

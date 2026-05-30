
# 🔐 Auth Service API (FastAPI + PostgreSQL)

A production-style authentication backend built using FastAPI, SQLAlchemy, PostgreSQL, JWT, and bcrypt.

---

## 🚀 Features

- User Registration
- User Login
- JWT Access Token (30 min expiry)
- Refresh Token (7 days stored in DB)
- Logout (invalidate refresh token)
- Password hashing with bcrypt
- JWT Authentication
- PostgreSQL database integration
- Environment variable configuration

---

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Passlib / bcrypt
- Uvicorn
- python-dotenv

---

## 📂 Project Structure

app/
  api/
    auth.py
    users.py
  models/
    user.py
    token.py
  schemas/
    auth.py
    user.py
  core/
    config.py
    security.py
  db/
    database.py
  dependencies/
    auth.py
main.py

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Login user |
| POST | /auth/refresh | Generate new access token |
| POST | /auth/logout | Logout user |


## ⚙️ Setup Instructions

### 1. Install dependencies


## 📚 What I Learned

- Building REST APIs with FastAPI
- JWT Authentication
- Refresh Token Strategy
- Password Hashing with bcrypt
- PostgreSQL Integration
- SQLAlchemy ORM
- Dependency Injection in FastAPI
- Environment Variable Management
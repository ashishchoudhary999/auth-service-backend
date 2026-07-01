
# 🔐 Auth Service API (FastAPI + PostgreSQL)

A backend authentication service built using FastAPI, SQLAlchemy, PostgreSQL, JWT, and bcrypt. Implements registration, login, access/refresh token flow, and logout with token invalidation.

**Live API:** [https://your-app-name.onrender.com](https://your-app-name.onrender.com) *(replace with your actual Render URL)*
**Interactive Docs:** [https://your-app-name.onrender.com/docs](https://your-app-name.onrender.com/docs)

---

## 🚀 Try It

```bash
# Register a new user
curl -X POST https://your-app-name.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'

# Response
{
  "id": 1,
  "email": "test@example.com",
  "created_at": "2026-07-01T10:00:00Z"
}
```

```bash
# Login
curl -X POST https://your-app-name.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "8f14e45fceea167a5a36...",
  "token_type": "bearer"
}
```

---

## 🚀 Features

- User registration with email/password
- Login with JWT access token (30 min expiry)
- Refresh token (7 days, stored in DB, rotated on use)
- Logout (invalidates refresh token server-side)
- Password hashing with bcrypt
- Route protection via JWT dependency injection
- PostgreSQL database integration
- Environment-based configuration (no secrets in code)

---

## 🛠 Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Pydantic · JWT (python-jose) · Passlib/bcrypt · Uvicorn · python-dotenv

---

## 📂 Project Structure

```
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
```

---

## 📌 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| POST | /auth/register | Register a new user | No |
| POST | /auth/login | Login, returns access + refresh token | No |
| POST | /auth/refresh | Exchange refresh token for new access token | No (refresh token in body) |
| POST | /auth/logout | Invalidate refresh token | Yes |

---

## ⚙️ Setup Instructions

### 1. Clone and install dependencies
```bash
git clone https://github.com/ashishchoudhary999/auth-service-api.git
cd auth-service-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://user:password@localhost:5432/authdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Run database migrations
```bash
alembic upgrade head
```

### 4. Start the server
```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

---

## 🧠 Design Decisions

- **Refresh tokens stored in DB, not stateless** — allows immediate revocation on logout, unlike pure JWT refresh which can't be invalidated before expiry.
- **Short-lived access tokens (30 min)** — limits the exposure window if a token is leaked, while refresh tokens handle session continuity.
- **Passwords hashed with bcrypt, never stored or logged in plaintext.**
- **Config loaded via environment variables** — no secrets committed to the repo, deployable across environments without code changes.

---

## 📄 License

MIT
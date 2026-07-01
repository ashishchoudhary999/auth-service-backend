# 🔐 Auth Service API (FastAPI + PostgreSQL)

A backend authentication service built using FastAPI, SQLAlchemy, PostgreSQL, JWT, and bcrypt. Implements registration, login, access/refresh token flow, and logout with token invalidation and refresh token rotation.

Live API: https://auth-service-backend-nxvt.onrender.com (https://auth-service-backend-nxvt.onrender.com)
Interactive Docs: https://auth-service-backend-nxvt.onrender.com/docs


🚀 Try It

# Register a new user
curl -X POST https://auth-service-backend-nxvt.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "SecurePass123"}'

# Response
{
  "id": 1,
  "email": "test@example.com",
  "created_at": "2026-07-01T10:00:00Z"
}

# Login
curl -X POST https://auth-service-backend-nxvt.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "8f14e45fceea167a5a36...",
  "token_type": "bearer"
}

# Get current user (protected)
curl -X GET https://auth-service-backend-nxvt.onrender.com/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "id": 1,
  "username": "ashish",
  "email": "ashish@example.com",
  "created_at": "2026-07-01T10:00:00Z"
}

# Refresh token
curl -X POST https://auth-service-backend-nxvt.onrender.com/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your-refresh-token"}'

# Response
{
  "access_token": "new_eyJhbGci...",
  "refresh_token": "new_8f14e45f...",
  "token_type": "bearer"
}

# Logout
curl -X POST https://auth-service-backend-nxvt.onrender.com/auth/logout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"refresh_token": "your-refresh-token"}'

# Response
{
  "message": "Logged out successfully"
}

🚀 Features


User registration with username, email & password
Login with JWT access token (30 min expiry)
Refresh token (7 days, stored in DB, rotated on every use)
Logout — invalidates refresh token server-side
Password hashing with bcrypt (never stored in plaintext)
Route protection via HTTPBearer dependency injection
Clean Bearer token input in Swagger UI (Authorize 🔒 button)
PostgreSQL database integration
Environment-based configuration (no secrets in code)



🛠 Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Pydantic · JWT (python-jose) · bcrypt · Uvicorn · python-dotenv · Alembic




📂 Project Structure

app/
  api/
    auth.py         # Register, Login, Refresh, Logout endpoints
    users.py        # Protected /me endpoint
  models/
    user.py         # User DB model
    token.py        # RefreshToken DB model
  schemas/
    auth.py         # Request/response schemas
    user.py         # User output schema
  core/
    config.py       # Environment variable config
    security.py     # Hashing, JWT, HTTPBearer
  db/
    database.py     # DB engine, session, Base
  dependencies/
    auth.py         # get_current_user dependency
main.py             # App entry point


📌 API Endpoints


Method	Endpoint	    Description	                           AuthRequired
GET	    /	            Health check	                       No
POST	/auth/register	Register a new user	                   No
POST	/auth/login	    Login, returns access + refresh token  No
POST	/auth/refresh	Exchange refresh token for new tokens  No        
POST	/auth/logout	Invalidate refresh token	           Yes
GET  	/users/me	    Get current logged-in user	               Yes


# How to Test in Swagger UI
Open https://auth-service-backend-nxvt.onrender.com/docs
Call POST /auth/register to create a user
Call POST /auth/login → copy the access_token
Click the 🔒 Authorize button (top right)
Paste the token → click Authorize → click Close
Now call any protected route like GET /users/me ✅



# ⚙️ Setup Instructions

1. Clone and install dependencies

git clone https://github.com/ashishchoudhary999/auth-service-api.git
cd auth-service-backend
python -m venv venv
source venv/bin/activate   
# Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Configure environment variables

# Create a .env file in the root directory:

DATABASE_URL=postgresql://user:password@localhost:5432/authdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Generate a secure SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"

3. Start the server

uvicorn main:app --reload
API will be available at http://localhost:8000, docs at http://localhost:8000/docs

🧠 Design Decisions


Refresh tokens stored in DB, not stateless — allows immediate revocation on logout, unlike pure JWT refresh which can't be invalidated before expiry.
Refresh token rotation on every use — each /auth/refresh call issues a brand new refresh token and invalidates the old one, preventing replay attacks.
Short-lived access tokens (30 min) — limits the exposure window if a token is leaked, while refresh tokens handle session continuity.
HTTPBearer over OAuth2PasswordBearer — gives a clean, simple "paste token" box in Swagger UI instead of a confusing OAuth2 form.
bcrypt used directly — passlib is unmaintained and incompatible with Python 3.14+, so bcrypt is used directly for future-proof password hashing.
Config loaded via environment variables — no secrets committed to the repo, deployable across environments without code changes.


📄 License

MIT
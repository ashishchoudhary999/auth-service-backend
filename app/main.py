from fastapi import FastAPI

from app.db.database import Base, engine

from app.api.auth import router as auth_router
from app.api.users import router as users_router


# -------------------------
# CREATE TABLES
# -------------------------
Base.metadata.create_all(bind=engine)


# -------------------------
# APP INIT
# -------------------------
app = FastAPI(
    title="Auth Service API",
    version="1.0.0"
)


# -------------------------
# ROUTERS
# -------------------------
app.include_router(auth_router)
app.include_router(users_router)


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"message": "Auth Service Running 🚀"}
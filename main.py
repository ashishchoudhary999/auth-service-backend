from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    version="1.0.0",
    description="JWT Authentication service with refresh token rotation",
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTERS
# -------------------------
app.include_router(auth_router)
app.include_router(users_router)


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/", tags=["Health"])
def root():
    return {"message": "Auth Service Running 🚀"}
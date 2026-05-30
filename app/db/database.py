from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL


# -------------------------
# DATABASE ENGINE
# -------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)


# -------------------------
# SESSION LOCAL
# -------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------
# BASE MODEL
# -------------------------
Base = declarative_base()


# -------------------------
# DEPENDENCY (DB SESSION)
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
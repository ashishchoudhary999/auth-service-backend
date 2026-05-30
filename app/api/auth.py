from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets

from app.db.database import get_db
from app.models.user import User
from app.models.token import RefreshToken

from app.schemas.auth import UserCreate, UserLogin

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# REGISTER
# -------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # ACCESS TOKEN (30 min)
    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    # REFRESH TOKEN (7 days)
    refresh_token = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(days=7)

    db_refresh = RefreshToken(
        user_id=db_user.id,
        token=refresh_token,
        expires_at=expires_at
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post("/refresh")
def refresh(token: str, db: Session = Depends(get_db)):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = db.query(User).filter(User.id == db_token.user_id).first()

    new_access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return {"message": "Logged out successfully"}
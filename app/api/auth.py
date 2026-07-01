from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import secrets

from app.db.database import get_db
from app.models.user import User
from app.models.token import RefreshToken

from app.schemas.auth import (
    UserCreate,
    UserLogin,
    RefreshTokenRequest,
    TokenResponse
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.dependencies.auth import get_current_user
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# REGISTER
# -------------------------
@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at
    }


# -------------------------
# LOGIN  ✅ Normal JSON body login
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UserLogin,          # ✅ plain JSON { "email": ..., "password": ... }
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if not db_user or not verify_password(
        credentials.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": db_user.email})

    refresh_token = secrets.token_hex(32)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    # ✅ Delete old refresh tokens before issuing a new one
    db.query(RefreshToken).filter(
        RefreshToken.user_id == db_user.id
    ).delete()

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
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == request.refresh_token
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(db_token)
        db.commit()
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    user = db.query(User).filter(User.id == db_token.user_id).first()

    new_access_token = create_access_token(data={"sub": user.email})

    # ✅ Rotate refresh token on every use
    new_refresh_token = secrets.token_hex(32)
    db_token.token = new_refresh_token
    db_token.expires_at = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout")
def logout(
    request: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == request.refresh_token,
        RefreshToken.user_id == current_user.id
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return {"message": "Logged out successfully"}
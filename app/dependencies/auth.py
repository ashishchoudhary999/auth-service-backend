from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.db.database import get_db
from app.models.user import User
from app.core.config import SECRET_KEY, ALGORITHM


# IMPORTANT:
# tokenUrl MUST match your actual login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------
# GET CURRENT USER (PROTECTED ROUTES)
# -------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
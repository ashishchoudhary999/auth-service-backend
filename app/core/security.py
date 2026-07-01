from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
import bcrypt

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# ✅ HTTPBearer for Swagger UI "paste token" box
http_bearer = HTTPBearer()


# -------------------------
# HASH PASSWORD
# -------------------------
def hash_password(password: str) -> str:
    # ✅ bcrypt directly — no passlib
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


# -------------------------
# VERIFY PASSWORD
# -------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # ✅ bcrypt directly — no passlib
    pwd_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


# -------------------------
# CREATE ACCESS TOKEN
# -------------------------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# -------------------------
# VERIFY ACCESS TOKEN
# -------------------------
def verify_access_token(token: str) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        return email

    except JWTError:
        raise credentials_exception
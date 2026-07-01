from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
import warnings

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# ✅ Suppress passlib bcrypt warning
warnings.filterwarnings("ignore", ".*error reading bcrypt version.*")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

http_bearer = HTTPBearer()


# -------------------------
# HASH PASSWORD
# -------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# -------------------------
# VERIFY PASSWORD
# -------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


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
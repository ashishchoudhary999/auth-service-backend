from passlib.context import CryptContext
import hashlib
from datetime import datetime, timedelta
from jose import jwt

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------
# PASSWORD NORMALIZATION
# ----------------------------
def _normalize_password(password: str) -> str:
    """
    Bcrypt has 72-byte limit.
    We pre-hash to avoid issues and ensure consistency.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ----------------------------
# PASSWORD HASHING
# ----------------------------
def hash_password(password: str) -> str:
    normalized = _normalize_password(password)

    print("Length:", len(normalized))
    print("Normalized:", normalized)

    return pwd_context.hash(normalized)


# ----------------------------
# PASSWORD VERIFY
# ----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    normalized = _normalize_password(plain_password)
    return pwd_context.verify(normalized, hashed_password)


# ----------------------------
# JWT TOKEN
# ----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
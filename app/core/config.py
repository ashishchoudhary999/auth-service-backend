import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# DATABASE
# -------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------
# JWT SETTINGS
# -------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-change-in-prod")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
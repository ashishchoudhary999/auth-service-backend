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
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
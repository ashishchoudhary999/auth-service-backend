from pydantic import BaseModel, EmailStr
from datetime import datetime


# -------------------------
# RESPONSE SCHEMA (SAFE OUTPUT)
# -------------------------
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
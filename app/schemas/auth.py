from pydantic import BaseModel, EmailStr


# -------------------------
# REGISTER
# -------------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# -------------------------
# LOGIN
# -------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str
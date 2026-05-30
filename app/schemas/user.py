from pydantic import BaseModel, EmailStr


# -------------------------
# RESPONSE SCHEMA (SAFE OUTPUT)
# -------------------------
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
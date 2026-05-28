from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.db.database import get_db

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email
    )

    # Add user to database
    db.add(new_user)

    # Save changes permanently
    db.commit()

    return {
        "message": "User created successfully"
    }
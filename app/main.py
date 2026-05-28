from fastapi import FastAPI

from app.db.database import engine, Base
from app.models.user import User

from app.api.user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Auth Service Running"}
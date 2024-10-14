from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Home
from db_engine import SessionLocal, initialize_db, input_sample_data
from user_repository import get_all_users, get_user_by_id, get_user_by_username
from contextlib import asynccontextmanager


# Initialize DB (create tables on startup - in memory DB)
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield
    input_sample_data()


# This will get the DB Session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)

# Routes


@app.get("/users/")
def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_all_users(db)[skip : skip + limit]
    return users


@app.get("/user/id/{user_id}")
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_username(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found by id")
    return user


@app.get("/user/name/{username}")
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found by username")
    return user

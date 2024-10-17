from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pyd_models import UserResponse, UserCreate
from db_engine import get_db
from user_repository import (
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    save_user,
)
from sqlalchemy.ext.asyncio import AsyncSession

# FASTAPI

app = FastAPI()

# Routes


@app.get(
    "/users/", response_model=list[UserResponse]
)  # Definimos el modelo de respuesta
async def read_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return users


@app.get(
    "/user/id/{user_id}", response_model=UserResponse
)  # Definimos el modelo de respuesta
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found by id")
    return user


@app.get(
    "/user/name/{username}", response_model=UserResponse
)  # Definimos el modelo de respuesta
async def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = await get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found by username")
    return user


@app.post("/user/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = await save_user(db, user)
    return created_user

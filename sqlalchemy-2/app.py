from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pyd_models import UserResponse
from db_engine import get_db
from user_repository import get_all_users, get_user_by_id, get_user_by_username
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

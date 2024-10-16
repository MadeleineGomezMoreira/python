from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str
    activated: Optional[bool] = False
    activation_date: Optional[datetime] = None
    activation_code: Optional[str] = None

    class Config:
        orm_mode = (
            True  # Esto permite a Pydantic leer datos desde los modelos de SQLAlchemy
        )


class UserCreate(UserBase):
    password: str  # La contraseña debe ser obligatoria en la creación


class UserResponse(UserBase):
    id: int  # Este campo será retornado cuando devuelvas un usuario existente
    homes: Optional[List["HomeResponse"]] = (
        []
    )  # Usarás esto cuando devuelvas relaciones con otros objetos

    class Config:
        orm_mode = True


class HomeBase(BaseModel):
    home_name: str

    class Config:
        orm_mode = True


class HomeCreate(HomeBase):
    pass  # No se requiere ningún campo adicional para crear un hogar


class HomeResponse(HomeBase):
    id: int
    owned_by: int  # Mostrará el ID del usuario que posee este hogar

    class Config:
        orm_mode = True

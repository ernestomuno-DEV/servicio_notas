from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import time
from typing import Literal

class Token(BaseModel):
    access_token: str
    token_type: str

class CrearUsuario(BaseModel):
    Email: EmailStr
    Password: str

class LeerUsuario(BaseModel):
    id: int
    Email: EmailStr
    Activo: bool

    model_config = ConfigDict(from_atributes = True)

class CrearNotas(BaseModel):
    Titulo:str
    Descripcion:str
    Limite : time
    Clasificacion: Literal["Trabajo", "Personal"]
    Completada: bool = False

class actualizarNotas(BaseModel):
    Titulo:str| None = None
    Descripcion:str | None = None
    Limite : time | None = None
    Clasificacion: Literal["Trabajo", "Personal"] | None = None
    Completada: bool | None = None


class LeerNotas(CrearNotas):
    id: int

    class Config:
        from_attributes = True
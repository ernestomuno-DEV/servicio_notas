from pydantic import BaseModel
from datetime import time
from typing import Literal

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
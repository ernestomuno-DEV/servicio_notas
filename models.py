from sqlalchemy import Column, Integer, String, Float, Boolean, Time
from db import Base
from datetime import time

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    Email = Column(String, unique=True, index=True, nullable=False)
    Password = Column(String, nullable = False)
    Activo = Column(Boolean, default=True)


class Notas(Base):
    __tablename__ = "notas"

    id= Column(Integer, primary_key=True, index=True)
    Titulo = Column(String, index=True)
    Descripcion = Column(String, index=True)
    Limite = Column(Time,index=True)
    Clasificacion = Column(String, index = True)
    Completada = Column(Boolean, index= True)

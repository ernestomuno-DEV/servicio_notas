from sqlalchemy import Column, Integer, String, Float, Boolean, Time
from db import Base
from datetime import time


class Notas(Base):
    __tablename__ = "notas"

    id= Column(Integer, primary_key=True, index=True)
    Titulo = Column(String, index=True)
    Descripcion = Column(String, index=True)
    Limite = Column(Time,index=True)
    Clasificacion = Column(String, index = True)
    Completada = Column(Boolean, index= True)

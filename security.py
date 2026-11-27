from pwdlib import PasswordHash
import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
import models
from db import get_db


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def encriptar_contraseña(contraseña_plana: str) -> str:
    return password_hash.hash(contraseña_plana)

def validar_contraseña(contraseña_plana: str, contraseña_hasheada: str) ->bool:
    return password_hash.verify(contraseña_plana, contraseña_hasheada)

def crear_token_acceso(datos: dict) -> str:
    datos_a_codificar = datos.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_codificar.update({"exp": expiracion})

    token_jwt = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def obtener_usuario_actual(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            print("DEBUG JWT: 'sub' vino vacío en el payload:", payload)
            raise credenciales_invalidas
    except jwt.PyJWTError as e:
        print("DEBUG JWT ERROR:", type(e).__name__, str(e))
        raise credenciales_invalidas

    usuario = db.query(models.Usuarios).filter(models.Usuarios.Email == email).first()
    if usuario is None:
        print("DEBUG DB: No se encontró el correo:", email)
        raise credenciales_invalidas
    if not usuario.Activo:
        print("DEBUG DB: El usuario tiene Activo =", usuario.Activo)
        raise credenciales_invalidas

    return usuario
from pwdlib import PasswordHash
import os
from datetime import datetime, timedelta, timezone
import jwt


password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRETE_KEY", "mysecretkey")
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
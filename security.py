from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def encriptar_contraseña(contraseña_plana: str) -> str:
    return password_hash.hash(contraseña_plana)

def validar_contraseña(contraseña_plana: str, contraseña_hasheada: str) ->bool:
    return password_hash.verify(contraseña_plana, contraseña_hasheada)
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, security
from db import get_db, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Notas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def saludo():
    return {'Saludo': 'Hola mundo'}

@app.post("/usuarios/", response_model=schemas.LeerUsuario, status_code = status.HTTP_201_CREATED)
def crear_usuario(usuario:schemas.CrearUsuario, db:Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuarios).filter(models.Usuarios.Email == usuario.Email).first()
    if usuario_existente:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= "El usuario ya existe")

    contraseña_segura = security.encriptar_contraseña(usuario.Password)

    nuevo_usuario = models.Usuarios(
        Email = usuario.Email,
        Password = contraseña_segura
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.post("/notas/", response_model=schemas.LeerNotas)
def crear_nota(nota: schemas.CrearNotas,db: Session = Depends(get_db)):
    nueva_nota = models.Notas(**nota.model_dump())
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota

@app.get("/notas/", response_model=list[schemas.LeerNotas])
def leer_notas(db:Session = Depends(get_db)):
    return db.query(models.Notas).order_by(models.Notas.Clasificacion, models.Notas.Limite).all()

@app.patch("/notas/{nota_id}", response_model=schemas.LeerNotas)
def actualizar_nota(
    nota_id:int,
    nota_actualizada: schemas.actualizarNotas,
    db:Session = Depends(get_db)
):
    nota_db = db.query(models.Notas).filter(models.Notas.id == nota_id).first()
    if not nota_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    datos_nuevos = nota_actualizada.model_dump(exclude_unset=True)

    for campo,valor in datos_nuevos.items():
        setattr(nota_db,campo,valor)

    db.commit()
    db.refresh(nota_db)
    return nota_db


@app.delete("/notas/{nota_id}", status_code= status.HTTP_204_NO_CONTENT)
def eliminar_nota(
    nota_id:int,
    db:Session = Depends(get_db)
):

    nota_db = db.query(models.Notas).filter(models.Notas.id == nota_id).first()

    if not nota_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    db.delete(nota_db)
    db.commit()
    return None
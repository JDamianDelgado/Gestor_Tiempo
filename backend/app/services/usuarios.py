from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.models.usuario import Usuario
from app.schemas.usuario import usuario_create, usuario_update

def crear_usuario(db:Session, datos:usuario_create):
    email= db.query(Usuario).filter(Usuario.email == datos.email.lower()).first()
    dni = db.query(Usuario).filter(Usuario.dni == datos.dni).first()

    if email: 
        raise HTTPException(status_code=400, detail="Datos ya registrados")
    elif dni:
        raise HTTPException(status_code=400, detail="Datos ya registrados")
    else:
        usuario = Usuario(email= datos.email.lower(), nombre=datos.nombre.title(), apellido= datos.apellido.title())

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

def listar_usuarios(db:Session):
    return db.query(Usuario).all()

def obtener_usuario_id(db:Session, id_usuario:int):
    usuario=  db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# def editar_usuario_id(db:Session, id_usuario:int,datos:usuario_update):
#     usuario= db.query(Usuario).filter(Usuario.id == id_usuario).first()
#     if not usuario:
#         raise HTTPException(status_code=404, detail='Usuario no encontrado')
#     else:
#         usuario.nombre = datos.nombre
#         usuario.email = datos.email
#         usuario.apellido= datos.apellido
#         usuario.dni= usuario.dni

#         db.commit()
#         db.refresh(usuario)
#         return usuario

def eliminar_user(db:Session, id_usuario:int):
    usuario= db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario :
        raise HTTPException(status_code=404,detail='No se pudo modificar usuario')
    else :
        db.delete(usuario)
        db.commit()
        return {'Usuario eliminado correctamente'}

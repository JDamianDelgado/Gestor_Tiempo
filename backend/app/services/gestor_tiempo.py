from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.models.gestor_tiempo import Gestor_tiempo
from app.schemas.gestor_tiempo import gestor_tiempo_create
from app.models.usuario import Usuario
from datetime import datetime
from app.google.sheets import registrar_actividad
def crear_registro(db:Session, datos:gestor_tiempo_create):
    usuario = db.query(Usuario).filter(Usuario.id == datos.usuario_id).first()
    if not usuario :
        raise HTTPException(status_code=404, detail='No se encontro al usuario')
    else:
        nombre_usuario = datos.usuario_nombre or f'{usuario.nombre} {usuario.apellido}'
        registro = Gestor_tiempo(
        paciente= datos.paciente,
        activity= datos.activity,
        usuario_id= datos.usuario_id,
        fecha_hora = datetime.now(),
        tiempo = datos.tiempo,
        modo_grupal = datos.modo_grupal
    )
        registrar_actividad(registro, nombre_usuario)
        db.add(registro)
        db.commit()
        db.refresh(registro)
        return registro

def all_register (db:Session):
    registros =  db.query(Gestor_tiempo).all()
    if not registros:
        raise HTTPException(status_code=404, detail='No se encontraron registros ')
    return registros 
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.gestor_tiempo import gestor_tiempo_create, gestor_tiempo_response
from app.services.gestor_tiempo import all_register, crear_registro


router= APIRouter(prefix='/registros',tags=['Registros'])

def get_db():
    db= SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model= gestor_tiempo_response)
def crear_registro_enpoint ( datos:gestor_tiempo_create, db:Session = Depends(get_db)):
    return crear_registro(db,datos)

@router.get('/all',response_model= list[gestor_tiempo_response])
def todos_registros(db:Session= Depends(get_db)):
    return all_register(db)
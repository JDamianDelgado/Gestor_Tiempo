from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.usuario import usuario_create, usuario_response, usuario_update
from app.services.usuarios import crear_usuario, listar_usuarios,obtener_usuario_id,eliminar_user
from app.google.importar_usuarios import importar_usuario_desde_sheet
from app.auth.security import require_sheets_admin

router = APIRouter(prefix='/usuarios',tags=['Usuarios'])

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model=usuario_response)
def crear_usuario_endpoint(
    datos:usuario_create,
    db:Session = Depends(get_db)
):
    return crear_usuario(db,datos)


@router.get('/', response_model=list[usuario_response])
def obtener_usuario(
        db:Session = Depends(get_db)
    ):
    return listar_usuarios(db)

@router.get("/{id_usuario}", response_model=usuario_response)
def obtener_usuario(id_usuario:int, db:Session=Depends(get_db)):
    return obtener_usuario_id(db, id_usuario)

# @router.put('/{id_usuario}', response_model=usuario_update)
# def editar_usuario(id_usuario:int, datos: usuario_update,db:Session=Depends(get_db)):
#     return editar_usuario_id(db, id_usuario, datos)

@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario:int, db:Session=Depends(get_db)):
    return eliminar_user(db,id_usuario)


@router.post("/importar-sheets", dependencies=[Depends(require_sheets_admin)])
def importar_sheets_usuarios(db:Session= Depends(get_db)):
    resultado = importar_usuario_desde_sheet(db)
    return resultado 

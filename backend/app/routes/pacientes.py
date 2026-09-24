from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.pacientes import paciente_response, paciente_filtrado
from app.routes.usuarios import get_db
from app.services.pacientes import lista_pacientes, filtrar_pacientes
from app.google.sheets import obtener_pacientes
from app.auth.security import require_sheets_admin
router= APIRouter(prefix="/pacientes", tags=["Pacientes"])

# @router.get("/", response_model=list[paciente_response])
# def listar_pacientes(db:Session= Depends(get_db)):
#     return listado_pacientes(db)

@router.get("/lista",response_model=list[paciente_filtrado])
def listado(db:Session=Depends(get_db)):
    return lista_pacientes(db)


@router.post("/sincronizar-sheets", response_model=list[paciente_filtrado], dependencies=[Depends(require_sheets_admin)])
def sincronizar_pacientes_desde_sheets():
    return filtrar_pacientes(obtener_pacientes())

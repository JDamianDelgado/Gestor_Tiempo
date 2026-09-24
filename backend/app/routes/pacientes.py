from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.pacientes import paciente_response, paciente_filtrado
from app.routes.usuarios import get_db
from app.services.pacientes import lista_pacientes
router= APIRouter(prefix="/pacientes", tags=["Pacientes"])

# @router.get("/", response_model=list[paciente_response])
# def listar_pacientes(db:Session= Depends(get_db)):
#     return listado_pacientes(db)

@router.get("/lista",response_model=list[paciente_filtrado])
def listado(db:Session=Depends(get_db)):
    return lista_pacientes(db)

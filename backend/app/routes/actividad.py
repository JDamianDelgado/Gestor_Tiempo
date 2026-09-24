from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.actividades import listado_Response
from app.services.actividades import listado_actividades
from app.routes.usuarios import get_db
router = APIRouter(prefix="/actividades", tags=[
    "Actividades"
])

@router.get("/", response_model= listado_Response)
def listar_actividades(db:Session= Depends(get_db)):
    return listado_actividades(db)


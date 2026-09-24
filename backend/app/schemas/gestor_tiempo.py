from pydantic import BaseModel
from app.models.usuario import Usuario
from datetime import datetime
from app.schemas.usuario import usuario_response
class gestor_tiempo_create(BaseModel):
    paciente:str
    activity:str
    usuario_id:int
    usuario_nombre:str | None = None
    tiempo:int
    modo_grupal:bool = False

class gestor_tiempo_response(BaseModel):
    id:int
    paciente:str
    activity:str
    usuario:usuario_response
    fecha_hora:datetime
    tiempo:int
    modo_grupal:bool


    class Config:
        from_attributes = True


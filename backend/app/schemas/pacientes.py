from pydantic import BaseModel
from datetime import datetime, date
class paciente_response(BaseModel):
    marca_temporal: str
    nombre_ingreso: str
    apellido: str
    fecha_ingreso: str
    nro_habitacion: int
    percepcion_sensorial: int
    exposicion_humedad: int
    actividad: int
    movilidad: int
    nutricion: int
    friccion: int
    braden: int
    riesgo: str

class paciente_filtrado(BaseModel):
    nombre_ingreso: str
    apellido:str
    nro_habitacion:int
    braden:int
    riesgo:str


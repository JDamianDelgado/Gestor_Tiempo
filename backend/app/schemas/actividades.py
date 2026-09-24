from typing import List, Dict
from pydantic import BaseModel

class Actividad(BaseModel):
    nombre:str

class Categoria_Actividad(BaseModel):
    categoria:str
    actividades: List[Actividad]

class listado_Response(BaseModel):
    categorias: list[Categoria_Actividad]
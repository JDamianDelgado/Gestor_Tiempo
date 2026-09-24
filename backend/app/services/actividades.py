from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.google.sheets import obtener_hoja
from collections import defaultdict
from app.schemas.actividades import Categoria_Actividad, Actividad, listado_Response
def listado_actividades(db:Session):
    spredsheets = obtener_hoja()
    
    worksheets =spredsheets.worksheet('ACTIVIDADES_LISTA')

    if not worksheets:
        raise HTTPException(status_code=402, detail="Hoja no encontrada")

    else:
        actividades= worksheets.get_all_records()
        actividades_por_categoria = defaultdict(list)

        for act in actividades:
            categoria= act.get('CATEGORIA')
            actividad = act.get('ACTIVIDADES')
            if categoria and actividad:
                actividades_por_categoria[categoria].append(actividad)
    categorias= []
    for categ ,acts in actividades_por_categoria.items():
        categorias.append(
            Categoria_Actividad(
                categoria = categ, 
                actividades = [Actividad(nombre=a) for a in acts]
            )
        )
    
    return listado_Response(categorias=categorias)

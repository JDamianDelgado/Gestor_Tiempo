from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.schemas.pacientes import paciente_response,paciente_filtrado
from app.google.sheets import obtener_pacientes

# def listado_pacientes(db:Session):
#     pacientes = obtener_pacientes()
#     return pacientes

def lista_pacientes(db:Session):
    return filtrar_pacientes(obtener_pacientes())


def filtrar_pacientes(pacientes):
    filtro =[]
    for i in pacientes:
        paciente=paciente_filtrado(
            nombre_ingreso=i.nombre_ingreso,
            apellido=i.apellido,
            nro_habitacion=i.nro_habitacion,
            braden=i.braden,
            riesgo=i.riesgo
        )
        filtro.append(paciente)
    return filtro

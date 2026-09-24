import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials
from app.schemas.usuario import usuario_create
from sqlalchemy.orm import Session
from pydantic import ValidationError
from datetime import datetime
from app.schemas.pacientes import paciente_response, paciente_filtrado
from dotenv import load_dotenv
import os
import json
load_dotenv()

google_credentials= os.getenv("GOOGLE_CREDENTIALS_JSON")

info= json.loads(google_credentials)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(info, scopes=SCOPES)

client= gspread.authorize(credentials)

def obtener_hoja():
    spreadsheet = client.open("DEMO - USUARIOS")
    return spreadsheet

def obtener_usuarios():
    spredsheets = obtener_hoja()
    worksheets= spredsheets.sheet1
    usuarios = worksheets.get_all_records()
    return usuarios

def obtener_pacientes():
    spredsheets = obtener_hoja()
    worksheets = spredsheets.worksheet("PACIENTES_LISTADO")
    registros = worksheets.get_all_records()
    pacientes = []
    for r in registros:
        paciente = paciente_response(
            marca_temporal=r["Marca temporal"],
            nombre_ingreso=str(r["Nombre del ingreso"]),
            apellido=str(r["Apellido"]),
            fecha_ingreso=r["Fecha de Ingreso"],
            nro_habitacion=r["Nro de Habitacion"],
            percepcion_sensorial=r["PERCEPCION SENSORIAL"],
            exposicion_humedad=r["EXPOSICION A LA HUMEDAD"],
            actividad=r["ACTIVIDAD"],
            movilidad=r["MOVILIDAD"],
            nutricion=r["NUTRICION"],
            friccion=r["FRICCION"],
            braden=r["BRADEN"],
            riesgo=r["RIESGO"] 
        )
        pacientes.append(paciente)
    return pacientes




def agregar_error(error_dict,detalle_error):
    spreadsheet = obtener_hoja()
    try:
        worksheet = spreadsheet.worksheet("Errores importacion")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Errores importacion", rows=100, cols=5)

    worksheet.append_row([error_dict["nombre"], error_dict["apellido"], error_dict["email"],datetime.now().strftime("%d-%b-%Y %H:%M:%S"), detalle_error], value_input_option="USER_ENTERED")
    return "Error agregado"

def registrar_actividad(actividad, usuario_nombre=None):
    spreadsheet= obtener_hoja()

    try:
        worksheet = spreadsheet.worksheet(title="REGISTRO ACTIVIDADES")
    except gspread.WorksheetNotFound:
        worksheet= spreadsheet.add_worksheet(title="REGISTRO ACTIVIDADES", rows=100,cols=6)
    worksheet.append_row([
        actividad.paciente,
        actividad.activity,
        usuario_nombre,
        actividad.fecha_hora.strftime("%d-%b-%Y %H:%M:%S"),
        actividad.tiempo,
        actividad.modo_grupal,
    ], value_input_option="USER_ENTERED")
    return "actividad agregada"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.connection import engine
from sqlalchemy import text
from app.models.usuario import Usuario
from app.models.gestor_tiempo import Gestor_tiempo
from app.routes.usuarios import router as usuario_router
from app.routes.gestor_tiempo import router as gestor_tiempo_router
from app.routes.actividad import router as actividad_router
from app.routes.pacientes import router as paciente_router
from app.auth.routes import router as auth_router
app = FastAPI()
from dotenv import load_dotenv
import os
load_dotenv()

URL_FRONTEND=os.getenv("URL_FRONTEND")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173",URL_FRONTEND],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(usuario_router)
app.include_router(gestor_tiempo_router)
app.include_router(actividad_router)
app.include_router(paciente_router)
app.include_router(auth_router)
@app.get('/')
def inicio():

    
    with engine.connect() as connection:
        resultado = connection.execute(
            text("SELECT 1")
        )
        valor = resultado.scalar()

    Base.metadata.create_all(bind=engine)

    return{
            'mensaje': 'conexion funcionando', 
            'resultado': valor
        }
from app.routes.usuarios import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException
from app.database.connection import SessionLocal
from app.auth.schemas import TokenResponse, LoginRequest
from app.auth.security import crear_token
from app.models.usuario import Usuario


router= APIRouter(prefix="/auth",tags=['Authentication'])

@router.post("/login", response_model= TokenResponse)
def login (datos:LoginRequest, db:Session=Depends(get_db)):
    usuario= db.query(Usuario).filter(Usuario.email == datos.email).first()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Datos incorrectos")
    if usuario.dni != int(datos.password):
        raise HTTPException(status_code=401, detail="Datos incorrectos")
    token= crear_token(usuario.id, usuario.email)

    return {
        "access_token": token,
        "token_type": "bearer"

    }
from pwdlib import PasswordHash
import os 
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM= 'HS256'
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
SHEETS_ADMIN_EMAIL = "joako@mail.com"
bearer_scheme = HTTPBearer()

def crear_token(usuario_id:int, email:str):
    payload= {
        "sub": str(usuario_id),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    token= jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def require_sheets_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        ) from error

    if payload.get("email", "").lower() != SHEETS_ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para importar usuarios.",
        )

    return payload
# password_hash = PasswordHash.recommended()

# def crear_password_hash(password:str):
#     return password_hash.hash(password)

# def verificar_password(password:str, password_hash_guardado:str):

#     return password_hash.verify(password, password_hash_guardado)

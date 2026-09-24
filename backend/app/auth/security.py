from pwdlib import PasswordHash
import os 

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM= 'HS256'

def crear_token(usuario_id:int, email:str):
    payload= {
        "sub": str(usuario_id),
        "email": email
    }

    token= jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
# password_hash = PasswordHash.recommended()

# def crear_password_hash(password:str):
#     return password_hash.hash(password)

# def verificar_password(password:str, password_hash_guardado:str):

#     return password_hash.verify(password, password_hash_guardado)

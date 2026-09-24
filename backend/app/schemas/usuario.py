from pydantic import BaseModel,EmailStr

class usuario_create(BaseModel):
    email:EmailStr
    nombre:str
    apellido:str
    dni:int

class usuario_response(BaseModel):
    id:int
    nombre:str
    apellido:str
    email:EmailStr
    dni:int
    class Config:
        from_attributes= True

class usuario_update(BaseModel):
    email:EmailStr
    nombre:str
    apellido:str
    dni:int
    
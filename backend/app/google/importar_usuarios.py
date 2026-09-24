from sqlalchemy.orm import Session
from pydantic import ValidationError 
import re
from app.google.sheets import obtener_usuarios,agregar_error
from app.schemas.usuario import usuario_create
from app.models.usuario import Usuario

def importar_usuario_desde_sheet(db:Session):
    usuarios= obtener_usuarios()
    email_procesados = set()
    importados = []
    no_importados = []
    duplicados = []
    email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    for i in usuarios:

        if (not i["apellido"].strip() or not i["nombre"].strip() or not i["email"].strip() or not email_regex.match(i["email"])):
            no_importados.append(i)
            agregar_error(i, "Datos incorrectos ")
            continue
        
        try :
            usuario_validado = usuario_create(
                nombre= i["nombre"],
                apellido = i["apellido"],
                email= i["email"],
                dni= i['dni']
            )
        except ValidationError as error:
            no_importados.append(i)
            agregar_error(i, str(error))
            continue

        if usuario_validado.email in email_procesados:
            duplicados.append(i)
            agregar_error(i , 'Email duplicado en Sheets')
            continue
        email_procesados.add(usuario_validado.email)

        usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_validado.email).first()

        if usuario_existente: 
            duplicados.append(i)
            continue

        nuevo_usuario = Usuario(
            nombre = usuario_validado.nombre, 
            apellido = usuario_validado.apellido,
            email = usuario_validado.email, 
            dni= usuario_validado.dni
        )
        db.add(nuevo_usuario)
        importados.append(usuario_validado)

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise

    return {"encontrados": len(usuarios),
            "importados": len(importados),
            "invalidos": len(no_importados),
            "duplicados": len(duplicados)}

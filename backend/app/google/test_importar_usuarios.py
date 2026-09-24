from app.database.connection import SessionLocal
from app.google.importar_usuarios import importar_usuario_desde_sheet


db = SessionLocal()

try:

    resultado = importar_usuario_desde_sheet(db)

    print("==============================")
    print("IMPORTACIÓN FINALIZADA")
    print("==============================")

    print(f"Encontrados: {resultado['encontrados']}")
    print(f"Importados: {resultado['importados']}")
    print(f"Inválidos: {resultado['invalidos']}")
    print(f"Duplicados: {resultado['duplicados']}")

finally:

    db.close()
from app.auth.security import (
    crear_password_hash,
    verificar_password
)


password = "30123456"

hash_generado = crear_password_hash(password)

print("PASSWORD ORIGINAL:")
print(password)

print()

print("HASH:")
print(hash_generado)

print()

print("PASSWORD CORRECTA:")
print(
    verificar_password(
        password,
        hash_generado
    )
)

print()

print("PASSWORD INCORRECTA:")
print(
    verificar_password(
        "99999999",
        hash_generado
    )
)
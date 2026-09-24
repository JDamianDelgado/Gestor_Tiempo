from app.google.sheets import obtener_hoja, obtener_usuarios

usuarios = obtener_usuarios()

print('Usuarios obtenidos')

for usuario in usuarios:
    print(usuario)
# Login/utils.py
import random
import string
import unicodedata

# ------------------------------------------------------------------------------------------------------------------ #

def Generar_Carnet(objeto, campo='carnet_alumno'):

    if getattr(objeto, campo):
        return  # Si tiene carnet, no hacer nada

    modelo = objeto.__class__
    ultimo = modelo.objects.order_by(f'-{campo}').first()
    
    if ultimo and getattr(ultimo, campo).isdigit():
        nuevo_carnet = str(int(getattr(ultimo, campo)) + 1)
    else:
        nuevo_carnet = '1111'
    
    setattr(objeto, campo, nuevo_carnet)

# ------------------------------------------------------------------------------------------------------------------ #

def Generar_Contrasenia(usuario, contrasena_field='contrasena_alumno'):

    if getattr(usuario, contrasena_field):
        return  # Si ya tiene contraseña, no hacer nada

    # Detecta el nombre y apellido según el modelo
    nombre = getattr(usuario, 'nombre_alumno', None) or getattr(usuario, 'nombre_maestro', '')
    apellido = getattr(usuario, 'apellido_alumno', None) or getattr(usuario, 'apellido_maestro', '')

    # Función para eliminar tildes y caracteres especiales
    def quitar_tildes(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    nombre = quitar_tildes(nombre)
    apellido = quitar_tildes(apellido)

    # Crear contraseña con primeras 2 letras de nombre + primeras 2 de apellido + 2 números aleatorios
    letras = (nombre[:2] + apellido[:2]).upper()
    numeros = ''.join(random.choices(string.digits, k=2))

    setattr(usuario, contrasena_field, letras + numeros)

# ------------------------------------------------------------------------------------------------------------------ #
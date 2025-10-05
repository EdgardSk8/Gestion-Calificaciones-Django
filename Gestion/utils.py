# Login/utils.py

import random
import string
import unicodedata

# ------------------------------------------------------------------------------------------------------------------ #

def generar_carnet(usuario, campo='carnet'):

    if getattr(usuario, campo):
        return  # Ya tiene carnet

    modelo = usuario.__class__
    ultimo = modelo.objects.order_by(f'-{campo}').first()

    if ultimo and getattr(ultimo, campo) and getattr(ultimo, campo).isdigit():
        nuevo_carnet = str(int(getattr(ultimo, campo)) + 1)
    else:
        nuevo_carnet = '1111'

    setattr(usuario, campo, nuevo_carnet)

# ------------------------------------------------------------------------------------------------------------------ #

def generar_contrasena(usuario, campo='contrasena'):

    if getattr(usuario, campo): # Ya tiene contraseña
        return  

    nombre = getattr(usuario, 'nombre', '')
    apellido = getattr(usuario, 'apellido', '')


    def quitar_tildes(texto): # Eliminar tildes y caracteres especiales
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    nombre = quitar_tildes(nombre)
    apellido = quitar_tildes(apellido)

    letras = (nombre[:2] + apellido[:2]).upper()
    numeros = ''.join(random.choices(string.digits, k=2))

    setattr(usuario, campo, letras + numeros)

# ------------------------------------------------------------------------------------------------------------------ #

def preparar_usuario(usuario):
    generar_carnet(usuario)
    generar_contrasena(usuario)

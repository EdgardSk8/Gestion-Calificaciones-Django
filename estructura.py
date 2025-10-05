import os

def mostrar_estructura(base_path, nivel=0):
    """Muestra la estructura de carpetas y archivos a partir de base_path."""
    prefijo = "    " * nivel + "|-- "
    for item in os.listdir(base_path):
        ruta_completa = os.path.join(base_path, item)
        print(prefijo + item)
        if os.path.isdir(ruta_completa):
            mostrar_estructura(ruta_completa, nivel + 1)

# Cambia '.' por la ruta de tu proyecto si no estás ejecutando desde la raíz
mostrar_estructura(".")

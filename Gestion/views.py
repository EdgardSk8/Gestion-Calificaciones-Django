from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Gestion.utils import preparar_usuario
from Login.models import Usuario # Importacion de modelo usuario

@csrf_exempt
def Nuevo_Usuario(request):
    """
    Crear un usuario (alumno, maestro o admin) vía JSON.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            nombre = data.get('nombre')
            apellido = data.get('apellido')
            rol = data.get('rol')  # 'alumno', 'maestro', 'admin'
            fecha_nacimiento = data.get('fecha_nacimiento')
            genero = data.get('genero')

            # Campos opcionales según rol
            anio_estudio = data.get('anio_estudio') if rol == 'alumno' else None
            estado = data.get('estado') if rol == 'alumno' else 'Activo'
            especialidad = data.get('especialidad') if rol == 'maestro' else None

            usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                rol=rol,
                fecha_nacimiento=fecha_nacimiento or None,
                genero=genero or None,
                anio_estudio=anio_estudio,
                estado=estado,
                especialidad=especialidad
            )

            # Generar carnet y contraseña
            preparar_usuario(usuario)
            usuario.save()

            return JsonResponse({
                'status': 'ok',
                'mensaje': f'Usuario creado correctamente',
                'usuario': {
                    'carnet': usuario.carnet,
                    'contrasena': usuario.contrasena,
                    'rol': usuario.rol,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'}, status=405)
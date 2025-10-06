# Gestion/controllers/Usuario_Controller.py
# Controlador basado en gestion de datos de la tabla Usuario

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Gestion.utils import preparar_usuario
from Login.models import Usuario # Importacion de modelo usuario

# ----------------------------------------------------------------------------------------------------- #

@csrf_exempt
def Nuevo_Usuario(request): # Creacion de nuevo usuario

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

# ----------------------------------------------------------------------------------------------------- #

@csrf_exempt
def ObtenerUsuarioID(request, id_usuario): # Obtener el ID de un Usuario

    # Verificar método permitido
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    # Verificar si el usuario ha iniciado sesión
    rol_sesion = request.session.get('rol')
    if not rol_sesion:
        return JsonResponse({'success': False, 'error': 'No ha iniciado sesión'}, status=401)

    try:
        # Buscar el usuario
        usuario = Usuario.objects.get(id_usuario=id_usuario)

        # Serializar datos básicos
        datos_usuario = {
            'id_usuario': usuario.id_usuario,
            'carnet': usuario.carnet,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'rol': usuario.rol,
            'fecha_nacimiento': usuario.fecha_nacimiento,
            'genero': usuario.genero,
            'anio_estudio': usuario.anio_estudio,
            'estado': usuario.estado,
            'especialidad': usuario.especialidad
        }

        return JsonResponse({'success': True, 'usuario': datos_usuario})

    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
    
# ----------------------------------------------------------------------------------------------------- #
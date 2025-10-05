# Login/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from .utils import Generar_Carnet, Generar_Contrasenia
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from Gestion.models import Maestro
from Gestion.models import Alumno

def Cargar_Login(request):
    return render(request, 'login/Login.html')

# ------------------------------------------------------------------------------------------------------------ #

def login_view(request):
    if request.method == "POST":
        carnet = request.POST.get("carnet")
        contrasena = request.POST.get("contrasena")

        # Primero buscamos si es Maestro
        try:
            usuario = Maestro.objects.get(carnet_maestro=carnet)
            if check_password(contrasena, usuario.contrasena_maestro):  # Contraseña encriptada
                # Guardar rol y usuario en sesión
                request.session['rol'] = 'maestro'
                request.session['usuario_id'] = usuario.id_maestro
                return redirect('dashboard_maestro')  # URL del panel de maestro
            else:
                messages.error(request, "Contraseña incorrecta")
                return redirect('login')
        except Maestro.DoesNotExist:
            pass

        # Si no es Maestro, buscamos Alumno
        try:
            usuario = Alumno.objects.get(carnet_alumno=carnet)
            if check_password(contrasena, usuario.contrasena_alumno):
                request.session['rol'] = 'alumno'
                request.session['usuario_id'] = usuario.id_alumno
                return redirect('dashboard_alumno')  # URL del panel de alumno
            else:
                messages.error(request, "Contraseña incorrecta")
                return redirect('login')
        except Alumno.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return redirect('login')

    # GET: mostrar formulario
    return render(request, 'login.html')

# ------------------------------------------------------------------------------------------------------------ #

@csrf_exempt  # Permite recibir POST sin token CSRF (solo para pruebas)
def Nuevo_Alumno(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido, usa POST'}, status=405)

    try:
        data = json.loads(request.body)  # Espera JSON con los datos del alumno
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # Campos requeridos
    required_fields = ['nombre_alumno', 'apellido_alumno', 'fecha_nacimiento_alumno', 'anio_estudio_alumno', 'genero_alumno']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'Falta el campo {field}'}, status=400)

    alumno = Alumno( # Creacion de objeto Alumno
        nombre_alumno = data['nombre_alumno'],
        apellido_alumno = data['apellido_alumno'],
        fecha_nacimiento_alumno = data['fecha_nacimiento_alumno'],
        anio_estudio_alumno = data['anio_estudio_alumno'],
        genero_alumno = data['genero_alumno']
    )

    # Generar carnet y contraseña
    Generar_Carnet(alumno)
    Generar_Contrasenia(alumno)

    alumno.save()# Guardar en DB

    return JsonResponse({
        'id_alumno': alumno.id_alumno,
        'carnet_alumno': alumno.carnet_alumno,
        'contrasena_alumno': alumno.contrasena_alumno,
        'nombre_alumno': alumno.nombre_alumno,
        'apellido_alumno': alumno.apellido_alumno,
        'fecha_nacimiento_alumno' : alumno.fecha_nacimiento_alumno,
        'anio_estudio_alumno' : alumno.anio_estudio_alumno,
        'genero_alumno' : alumno.genero_alumno,
        'estado' : alumno.estado

    }, status=201)

# ------------------------------------------------------------------------------------------------------------ #

@csrf_exempt
def Eliminar_Alumno(request, alumno_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido, usa DELETE'}, status=405)

    try:
        alumno = Alumno.objects.get(id_alumno=alumno_id)
        alumno.delete()
        return JsonResponse({'mensaje': f'Alumno con id {alumno_id} eliminado correctamente.'}, status=200)
    except Alumno.DoesNotExist:
        return JsonResponse({'error': f'No existe un alumno con id {alumno_id}'}, status=404)
    
# ------------------------------------------------------------------------------------------------------------ #

@csrf_exempt
def Cambiar_Estado_Alumno(request, alumno_id):
    if request.method != 'PUT' and request.method != 'PATCH':
        return JsonResponse({'error': 'Método no permitido, usa PUT o PATCH'}, status=405)

    try:
        alumno = Alumno.objects.get(id_alumno=alumno_id)
    except Alumno.DoesNotExist:
        return JsonResponse({'error': f'No existe un alumno con id {alumno_id}'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # Verificar que venga el campo estado
    nuevo_estado = data.get("estado")
    if nuevo_estado not in ['Activo', 'Egresado', 'Expulsado']:
        return JsonResponse({'error': 'Estado inválido. Usa: Activo, Egresado o Expulsado'}, status=400)

    # Actualizar estado
    alumno.estado = nuevo_estado
    alumno.save()

    return JsonResponse({
        'mensaje': f'El estado del alumno {alumno.nombre_alumno} {alumno.apellido_alumno} fue cambiado a {alumno.estado}',
        'id_alumno': alumno.id_alumno,
        'estado': alumno.estado
    }, status=200)

# ------------------------------------------------------------------------------------------------------------ #
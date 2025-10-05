# Login/views.py

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from Login.models import Usuario  # Modelo de Usuario

# ---------------------------------------------------------------------------------------------------- #

# Cargar formulario de login

def Cargar_Login(request):
    return render(request, 'login/Login.html')

# ---------------------------------------------------------------------------------------------------- #

# Login del usuario

@csrf_exempt
def login_usuario(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carnet = data.get('carnet')
            contrasena = data.get('contrasena')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

        try:
            usuario = Usuario.objects.get(carnet=carnet)

            # Verificar contraseña en texto plano
            if contrasena != usuario.contrasena:
                return JsonResponse({'success': False, 'error': 'Carnet o contraseña incorrectos'}, status=401)

            # Guardar rol en sesión
            request.session['rol'] = usuario.rol

            # Retornar solo rol
            return JsonResponse({
                'success': True,
                'rol': usuario.rol
            })

        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Carnet o contraseña incorrectos'}, status=401)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

# ---------------------------------------------------------------------------------------------------- #

# Vistas protegidas según rol

def vista_alumno_render(request): # Funcion que redirige hacia la vista de alumno
    if request.session.get('rol') != 'alumno':
        return redirect('/')  # Redirige al login si no es alumno
    return render(request, "gestion/alumno.html")

# ------------------------------------------------------------------ #

def vista_maestro_render(request): # Funcion que redirige hacia la vista de maestro
    if request.session.get('rol') != 'maestro':
        return redirect('/')  # Redirige al login si no es maestro
    return render(request, "gestion/maestro.html")

# ------------------------------------------------------------------ #

def vista_admin_render(request): # Funcion que redirige hacia la vista de administrador
    if request.session.get('rol') != 'admin':
        return redirect('/')  # Redirige al login si no es admin
    return render(request, "gestion/admin.html")

# ---------------------------------------------------------------------------------------------------- #

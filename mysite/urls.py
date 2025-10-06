# mysite/urls.py

from django.contrib import admin
from django.urls import path, include
from Login import views

urlpatterns = [
    
    # -------------------- End Point Principal -------------------- #

    path('', views.Cargar_Login, name='login'), # Al entrar a la web cargar Login

    # path('administrador/', admin.site.urls),
    path('login/', include('Login.urls')), # Todas las rutas de Login
    path('gestion/', include('Gestion.urls')), # Todas las rutas de Gestión

    # ------------------------------------------------------------- #
]

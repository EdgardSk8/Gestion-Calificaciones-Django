#Login/urls.py

from django.urls import path
from . import views 

urlpatterns = [
   path('', views.Cargar_Login, name='login'),
   path('login_usuario/', views.login_usuario, name='login_usuario'),  # Endpoint POST login

   path('vista_alumno/', views.vista_alumno_render, name='vista_alumno'),
   path('vista_maestro/', views.vista_maestro_render, name='vista_maestro'),
   path('vista_admin/', views.vista_admin_render, name='vista_admin'),

]

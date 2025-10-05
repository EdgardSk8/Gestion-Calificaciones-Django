#Login/urls.py

from django.urls import path
from . import views 

urlpatterns = [
   path('nuevo_alumno/', views.Nuevo_Alumno, name='nuevo_alumno'),
   path('alumno/<int:alumno_id>/eliminar_alumno/', views.Eliminar_Alumno, name='eliminar_alumno'),

   path('alumno/<int:alumno_id>/cambiar_estado_alumno/', views.Cambiar_Estado_Alumno, name='cambiar_estado_alumno'),

]

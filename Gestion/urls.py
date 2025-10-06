# Gestion/urls.py

from django.urls import path
from Gestion import views

urlpatterns = [

    # ------------------------------ End Point Usuarios ------------------------------ #

    path('nuevo_usuario/', views.Nuevo_Usuario, name='nuevo_usuario'),
    path('usuario/<int:id_usuario>/', views.ObtenerUsuarioID, name='obtenerusuarioid'),

    # -------------------------------------------------------------------------------- #
]

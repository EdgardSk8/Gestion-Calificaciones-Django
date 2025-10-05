# Gestion/urls.py

from django.urls import path
from Gestion import views


urlpatterns = [
    path('nuevo_usuario/', views.Nuevo_Usuario, name='nuevo_usuario'),
]

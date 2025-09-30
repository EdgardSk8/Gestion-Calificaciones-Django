
from django.urls import path
from . import views # Importacion de vistas en la misma carpeta ( . )

urlpatterns = [
    path('', views.hello), # En la vista principal, llamar con view a la funcion "hello"
]

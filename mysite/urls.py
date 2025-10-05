# mysite/urls.py

from django.contrib import admin
from django.urls import path, include
from Login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Login.urls')),
    path('gestion/', include('Gestion.urls')), 

    path('', views.Cargar_Login, name='login'),
]

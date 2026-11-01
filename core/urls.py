from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_inicio, name='api_inicio'),

    path(
        'usuarios/',
        views.listar_usuarios,
        name='listar_usuarios'
    ),

    path(
        'salas/',
        views.listar_salas,
        name='listar_salas'
    ),
]
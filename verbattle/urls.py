from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('matchmaking/', views.matchmaking, name='matchmaking'),
    path('duelo/', views.sala_duelo_directa, name='sala_duelo_directa'),
    path('duelo/<int:sala_id>/', views.sala_duelo, name='sala_duelo'),
    path('ranking/', views.ranking, name='ranking'),
    path('resultado/', views.resultado, name='resultado'),
]
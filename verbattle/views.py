from django.shortcuts import render, get_object_or_404
from .models import PerfilJugador, SalaVirtual, Pregunta

def home(request):
    """Lobby Principal del Jugador"""
    perfil, _ = PerfilJugador.objects.get_or_create(gamer_tag="Gamer_Estudiante")
    salas = SalaVirtual.objects.filter(estado='ESPERANDO')[:5]
    return render(request, 'home.html', {
        'perfil': perfil,
        'salas': salas
    })

def sala_duelo_directa(request):
    """Arena de Duelo 1vs1 Directa"""
    perfil, _ = PerfilJugador.objects.get_or_create(gamer_tag="Gamer_Estudiante")
    pregunta = Pregunta.objects.first()
    return render(request, 'sala_duelo.html', {
        'perfil': perfil,
        'pregunta': pregunta
    })

def sala_duelo(request, sala_id):
    """Arena de Duelo por Código de Sala"""
    perfil, _ = PerfilJugador.objects.get_or_create(gamer_tag="Gamer_Estudiante")
    sala = get_object_or_404(SalaVirtual, id=sala_id)
    pregunta = Pregunta.objects.first()
    return render(request, 'sala_duelo.html', {
        'perfil': perfil,
        'sala': sala,
        'pregunta': pregunta
    })

def ranking(request):
    """Tabla de Clasificación Global e-Sports"""
    perfil, _ = PerfilJugador.objects.get_or_create(gamer_tag="Gamer_Estudiante")
    jugadores = PerfilJugador.objects.all().order_by('-puntos_xp')
    return render(request, 'ranking.html', {
        'perfil': perfil,
        'jugadores': jugadores
    })

def resultado(request):
    """Resumen de Fin de Partida (Victoria / Derrota)"""
    perfil, _ = PerfilJugador.objects.get_or_create(gamer_tag="Gamer_Estudiante")
    return render(request, 'resultado.html', {
        'perfil': perfil
    })
from django.shortcuts import render, get_object_or_404
from .models import PerfilJugador, SalaVirtual, Pregunta

def get_perfil_activo():
    """Obtiene o crea el perfil principal del jugador en la BD"""
    perfil, _ = PerfilJugador.objects.get_or_create(
        id=1,
        defaults={
            'gamer_tag': 'Gamer_Estudiante',
            'nivel_dominio': 'BAJO',
            'puntos_xp': 0,
            'victorias': 0,
            'derrotas': 0
        }
    )
    return perfil

def home(request):
    """Lobby Principal del Jugador"""
    perfil = get_perfil_activo()

    # Si se envía el formulario desde Login o Registro, se actualiza el perfil en la BD
    if request.method == 'POST':
        gamer_tag = request.POST.get('gamer_tag')
        nivel_dominio = request.POST.get('nivel_dominio')

        if gamer_tag:
            perfil.gamer_tag = gamer_tag
        if nivel_dominio:
            perfil.nivel_dominio = nivel_dominio
        perfil.save()

    # Obtenemos las salas que están esperando oponente
    salas = SalaVirtual.objects.filter(estado='ESPERANDO')[:5]
    
    return render(request, 'home.html', {
        'perfil': perfil,
        'salas': salas
    })

def sala_duelo_directa(request):
    """Arena de Duelo 1vs1 Directa (Matchmaking)"""
    perfil = get_perfil_activo()
    # Obtenemos una pregunta aleatoria para que no sea siempre la misma
    pregunta = Pregunta.objects.order_by('?').first() 
    
    return render(request, 'sala_duelo.html', {
        'perfil': perfil,
        'pregunta': pregunta
    })

def sala_duelo(request, sala_id):
    """Arena de Duelo por Código de Sala"""
    perfil = get_perfil_activo()
    sala = get_object_or_404(SalaVirtual, id=sala_id)
    pregunta = Pregunta.objects.order_by('?').first()
    
    return render(request, 'sala_duelo.html', {
        'perfil': perfil,
        'sala': sala,
        'pregunta': pregunta
    })

def ranking(request):
    """Tabla de Clasificación Global e-Sports"""
    perfil = get_perfil_activo()
    # Ordenamos de mayor a menor puntaje para el podio
    jugadores = PerfilJugador.objects.all().order_by('-puntos_xp')
    
    return render(request, 'ranking.html', {
        'perfil': perfil,
        'jugadores': jugadores
    })

def resultado(request):
    """Resumen de Fin de Partida (Victoria / Derrota)"""
    perfil = get_perfil_activo()
    return render(request, 'resultado.html', {
        'perfil': perfil
    })

def login_view(request):
    """Pantalla de Iniciar Sesión"""
    perfil = get_perfil_activo()
    return render(request, 'login.html', {'perfil': perfil})

def registro_view(request):
    """Pantalla de Registro de Jugador"""
    perfil = get_perfil_activo()
    return render(request, 'registro.html', {'perfil': perfil})

def matchmaking(request):
    """Pantalla de Radar / Búsqueda de Oponente"""
    perfil = get_perfil_activo()
    return render(request, 'matchmaking.html', {'perfil': perfil})
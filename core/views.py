from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import PerfilJugador, SalaVirtual, Pregunta

# ==========================================
# 🚀 VISTAS PARA LAS PLANTILLAS HTML (FRONTEND)
# ==========================================

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

    if request.method == 'POST':
        gamer_tag = request.POST.get('gamer_tag')
        nivel_dominio = request.POST.get('nivel_dominio')

        if gamer_tag:
            perfil.gamer_tag = gamer_tag
        if nivel_dominio:
            perfil.nivel_dominio = nivel_dominio
        perfil.save()

    salas = SalaVirtual.objects.filter(estado='ESPERANDO')[:5]
    
    return render(request, 'home.html', {
        'perfil': perfil,
        'salas': salas
    })

def sala_duelo_directa(request):
    """Arena de Duelo 1vs1 Directa"""
    perfil = get_perfil_activo()
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
    jugadores = PerfilJugador.objects.all().order_by('-puntos_xp')
    
    return render(request, 'ranking.html', {
        'perfil': perfil,
        'jugadores': jugadores
    })

def resultado(request):
    """Resumen de Fin de Partida"""
    perfil = get_perfil_activo()
    return render(request, 'resultado.html', {
        'perfil': perfil
    })

def login_view(request):
    """Pantalla de Iniciar Sesión"""
    perfil = get_perfil_activo()
    return render(request, 'login.html', {'perfil': perfil})

def registro_view(request):
    """Pantalla de Registro"""
    perfil = get_perfil_activo()
    return render(request, 'registro.html', {'perfil': perfil})

def matchmaking(request):
    """Radar de Búsqueda"""
    perfil = get_perfil_activo()
    return render(request, 'matchmaking.html', {'perfil': perfil})


# ==========================================
# 🔌 VISTAS DE API (PRUEBAS DE BACKEND)
# ==========================================

def api_inicio(request):
    return JsonResponse({
        "proyecto": "Verbattle",
        "mensaje": "Backend funcionando correctamente",
        "estado": "activo",
        "version": "1.0"
    })

def listar_usuarios(request):
    usuarios = PerfilJugador.objects.all()
    datos = []
    for perfil in usuarios:
        datos.append({
            "id": perfil.id,
            "gamer_tag": perfil.gamer_tag,
            "puntos_xp": perfil.puntos_xp,
            "nivel": perfil.nivel_dominio
        })
    return JsonResponse({"estado": "correcto", "usuarios": datos})

def listar_salas(request):
    salas = SalaVirtual.objects.all()
    datos = []
    for sala in salas:
        datos.append({
            "id": sala.id,
            "codigo": sala.codigo_sala,
            "estado": sala.estado,
            "jugador1": sala.jugador1.gamer_tag if sala.jugador1 else None,
            "jugador2": sala.jugador2.gamer_tag if sala.jugador2 else None,
        })
    return JsonResponse({"estado": "correcto", "salas": datos})
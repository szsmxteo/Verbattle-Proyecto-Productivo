from django.http import JsonResponse

from .models import PerfilUsuario, SalaVirtual


def api_inicio(request):
    return JsonResponse({
        "proyecto": "Verbattle",
        "mensaje": "Backend funcionando correctamente",
        "estado": "activo",
        "version": "1.0"
    })


def listar_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related(
        'usuario'
    ).all()

    datos = []

    for perfil in usuarios:
        datos.append({
            "id": perfil.id,
            "nombre": perfil.nombre_completo,
            "puntaje": perfil.puntaje,
            "nivel": perfil.nivel
        })

    return JsonResponse({
        "estado": "correcto",
        "total_usuarios": len(datos),
        "usuarios": datos
    })


def listar_salas(request):
    salas = SalaVirtual.objects.select_related(
        'jugador_1',
        'jugador_2'
    ).all()

    datos = []

    for sala in salas:
        datos.append({
            "id": sala.id,
            "nombre": sala.nombre,
            "codigo": sala.codigo,
            "jugador_1": sala.jugador_1.nombre_completo,
            "jugador_2": (
                sala.jugador_2.nombre_completo
                if sala.jugador_2 else None
            ),
            "activa": sala.activa
        })

    return JsonResponse({
        "estado": "correcto",
        "total_salas": len(datos),
        "salas": datos
    })

from .models import RetoLinguistico


def listar_retos(request):
    retos = RetoLinguistico.objects.all()

    datos = []

    for reto in retos:
        datos.append({
            "id": reto.id,
            "idioma": reto.get_idioma_display(),
            "pregunta": reto.pregunta,
            "dificultad": reto.dificultad,
            "puntos": reto.puntos,
            "sala_id": reto.sala_id
        })

    return JsonResponse({
        "estado": "correcto",
        "total_retos": len(datos),
        "retos": datos
    })
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegistroForm
from .models import PerfilJugador, Pregunta, SalaVirtual

TIEMPO_LIMITE = 60      # segundos que dura cada pregunta
MARGEN_SEGUNDOS = 5     # tolerancia por la demora de la red
XP_POR_ACIERTO = 10


# ==========================================
# PERFIL DEL JUGADOR (uno por usuario)
# ==========================================

def get_perfil_activo(request):
    """Devuelve el perfil del usuario que inició sesión y actualiza su racha diaria."""
    perfil, _ = PerfilJugador.objects.get_or_create(
        usuario=request.user,
        defaults={"gamer_tag": request.user.username[:50]},
    )

    hoy = timezone.localdate()  # fecha según America/Bogota, no la del servidor
    if perfil.ultima_conexion != hoy:
        if perfil.ultima_conexion == hoy - timedelta(days=1):
            perfil.racha_actual += 1  # se conectó ayer: la racha sigue
        else:
            perfil.racha_actual = 1  # primera vez o se saltó días: empieza de nuevo
        perfil.ultima_conexion = hoy
        perfil.save(update_fields=["racha_actual", "ultima_conexion"])

    return perfil


# ==========================================
# REGISTRO, LOGIN Y LOGOUT
# ==========================================

def registro_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    errores = []
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            usuario = User.objects.create_user(
                username=datos["gamer_tag"],
                email=datos["email"],
                password=datos["password"],
            )
            PerfilJugador.objects.create(
                usuario=usuario,
                gamer_tag=datos["gamer_tag"],
                nivel_dominio=datos["nivel_dominio"],
            )
            login(request, usuario)
            return redirect("home")
        errores = [mensaje for lista in form.errors.values() for mensaje in lista]

    return render(request, "registro.html", {"errores": errores})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    next_url = request.POST.get("next") or request.GET.get("next", "")
    error = None

    if request.method == "POST":
        usuario = authenticate(
            request,
            username=request.POST.get("gamer_tag", "").strip(),
            password=request.POST.get("password", ""),
        )
        if usuario is not None:
            login(request, usuario)
            if url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("home")
        error = "GamerTag o contraseña incorrectos."

    return render(request, "login.html", {"error": error, "next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


# ==========================================
# DUELO: la respuesta se comprueba en el servidor
# ==========================================

def iniciar_duelo(request, pregunta):
    """Anota en la sesión qué pregunta se mostró y cuándo, para validar la respuesta."""
    if pregunta:
        request.session["duelo"] = {
            "pregunta_id": pregunta.id,
            "inicio": timezone.now().timestamp(),
            "respondida": False,
        }
    else:
        request.session.pop("duelo", None)


@login_required
@require_POST
def responder(request):
    """Comprueba la respuesta y guarda XP, victorias y derrotas."""
    duelo = request.session.get("duelo")
    if not duelo or duelo.get("respondida"):
        return JsonResponse({"error": "No hay una pregunta activa."}, status=400)

    pregunta = Pregunta.objects.filter(pk=duelo["pregunta_id"]).first()
    if pregunta is None:
        return JsonResponse({"error": "La pregunta ya no existe."}, status=400)

    opcion = request.POST.get("opcion", "").strip().upper()
    if opcion not in ("", "A", "B", "C", "D"):
        return JsonResponse({"error": "Opción no válida."}, status=400)

    # Se marca como respondida ANTES de dar puntos, para no cobrar dos veces.
    duelo["respondida"] = True
    request.session["duelo"] = duelo

    transcurrido = timezone.now().timestamp() - duelo["inicio"]
    a_tiempo = transcurrido <= TIEMPO_LIMITE + MARGEN_SEGUNDOS
    letra_correcta = pregunta.respuesta_correcta.strip().upper()

    if opcion == "" or not a_tiempo:
        estado = "tiempo"
    elif opcion == letra_correcta:
        estado = "correcta"
    else:
        estado = "incorrecta"

    perfil = get_perfil_activo(request)
    xp_ganado = XP_POR_ACIERTO if estado == "correcta" else 0
    if estado == "correcta":
        cambios = {
            "puntos_xp": F("puntos_xp") + xp_ganado,
            "victorias": F("victorias") + 1,
        }
    else:
        cambios = {"derrotas": F("derrotas") + 1}
    PerfilJugador.objects.filter(pk=perfil.pk).update(**cambios)
    perfil.refresh_from_db()

    return JsonResponse(
        {
            "estado": estado,
            "respuesta_correcta": letra_correcta,
            "xp_ganado": xp_ganado,
            "puntos_xp": perfil.puntos_xp,
            "victorias": perfil.victorias,
            "derrotas": perfil.derrotas,
        }
    )


# ==========================================
# VISTAS DE LAS PANTALLAS (requieren sesión)
# ==========================================

@login_required
def home(request):
    """Lobby Principal del Jugador"""
    perfil = get_perfil_activo(request)

    if request.method == "POST":
        gamer_tag = request.POST.get("gamer_tag", "").strip()[:50]
        nivel_dominio = request.POST.get("nivel_dominio")

        if gamer_tag:
            perfil.gamer_tag = gamer_tag
        if nivel_dominio in dict(PerfilJugador.NIVELES):
            perfil.nivel_dominio = nivel_dominio
        perfil.save()

    salas = SalaVirtual.objects.filter(estado="ESPERANDO")[:5]
    return render(request, "home.html", {"perfil": perfil, "salas": salas})


@login_required
def sala_duelo_directa(request):
    """Arena de Duelo 1vs1 Directa"""
    perfil = get_perfil_activo(request)
    pregunta = Pregunta.objects.order_by("?").first()
    iniciar_duelo(request, pregunta)
    return render(request, "sala_duelo.html", {"perfil": perfil, "pregunta": pregunta})


@login_required
def sala_duelo(request, sala_id):
    """Arena de Duelo por Código de Sala"""
    perfil = get_perfil_activo(request)
    sala = get_object_or_404(SalaVirtual, id=sala_id)
    pregunta = Pregunta.objects.order_by("?").first()
    iniciar_duelo(request, pregunta)
    return render(
        request,
        "sala_duelo.html",
        {"perfil": perfil, "sala": sala, "pregunta": pregunta},
    )


@login_required
def ranking(request):
    """Tabla de Clasificación Global e-Sports"""
    perfil = get_perfil_activo(request)
    jugadores = PerfilJugador.objects.all().order_by("-puntos_xp")
    return render(request, "ranking.html", {"perfil": perfil, "jugadores": jugadores})


@login_required
def resultado(request):
    """Resumen de Fin de Partida"""
    perfil = get_perfil_activo(request)
    return render(request, "resultado.html", {"perfil": perfil})


@login_required
def matchmaking(request):
    """Radar de Búsqueda"""
    perfil = get_perfil_activo(request)
    return render(request, "matchmaking.html", {"perfil": perfil})


# ==========================================
# VISTAS DE API (pruebas de backend, aún sin ruta en urls.py)
# ==========================================

def api_inicio(request):
    return JsonResponse(
        {
            "proyecto": "Verbattle",
            "mensaje": "Backend funcionando correctamente",
            "estado": "activo",
            "version": "1.0",
        }
    )


def listar_usuarios(request):
    datos = [
        {
            "id": perfil.id,
            "gamer_tag": perfil.gamer_tag,
            "puntos_xp": perfil.puntos_xp,
            "nivel": perfil.nivel_dominio,
            "racha": perfil.racha_actual,
        }
        for perfil in PerfilJugador.objects.all()
    ]
    return JsonResponse({"estado": "correcto", "usuarios": datos})


def listar_salas(request):
    datos = [
        {
            "id": sala.id,
            "codigo": sala.codigo_sala,
            "estado": sala.estado,
            "jugador1": sala.jugador1.gamer_tag if sala.jugador1 else None,
            "jugador2": sala.jugador2.gamer_tag if sala.jugador2 else None,
        }
        for sala in SalaVirtual.objects.all()
    ]
    return JsonResponse({"estado": "correcto", "salas": datos})

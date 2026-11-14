from datetime import timedelta
from types import SimpleNamespace

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import PerfilJugador
from .views import get_perfil_activo


def crear_jugador(nombre, clave="ClaveSegura#2026"):
    usuario = User.objects.create_user(username=nombre, password=clave)
    perfil = PerfilJugador.objects.create(usuario=usuario, gamer_tag=nombre)
    return usuario, perfil


class RegistroTests(TestCase):
    def datos(self, **cambios):
        datos = {
            "gamer_tag": "Nuevo_Gamer",
            "email": "nuevo@colegio.edu.co",
            "password": "ClaveSegura#2026",
            "nivel_dominio": "MEDIO",
        }
        datos.update(cambios)
        return datos

    def test_registro_crea_usuario_perfil_e_inicia_sesion(self):
        r = self.client.post(reverse("registro"), self.datos())
        self.assertRedirects(r, reverse("home"), fetch_redirect_response=False)
        usuario = User.objects.get(username="Nuevo_Gamer")
        self.assertEqual(usuario.perfiljugador.nivel_dominio, "MEDIO")
        self.assertIn("_auth_user_id", self.client.session)

    def test_registro_rechaza_gamertag_repetido(self):
        crear_jugador("Repetido")
        r = self.client.post(reverse("registro"), self.datos(gamer_tag="repetido"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_registro_rechaza_contrasena_debil(self):
        r = self.client.post(reverse("registro"), self.datos(password="1234"))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="Nuevo_Gamer").exists())


class LoginTests(TestCase):
    def setUp(self):
        crear_jugador("Oscar_QA")

    def test_login_correcto(self):
        r = self.client.post(
            reverse("login"), {"gamer_tag": "Oscar_QA", "password": "ClaveSegura#2026"}
        )
        self.assertRedirects(r, reverse("home"), fetch_redirect_response=False)

    def test_login_con_clave_incorrecta(self):
        r = self.client.post(
            reverse("login"), {"gamer_tag": "Oscar_QA", "password": "otra"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_no_redirige_a_sitios_externos(self):
        r = self.client.post(
            reverse("login"),
            {
                "gamer_tag": "Oscar_QA",
                "password": "ClaveSegura#2026",
                "next": "https://sitio-malicioso.com",
            },
        )
        self.assertRedirects(r, reverse("home"), fetch_redirect_response=False)

    def test_pantallas_exigen_sesion(self):
        for nombre in ["home", "ranking", "matchmaking", "resultado", "sala_duelo_directa"]:
            r = self.client.get(reverse(nombre))
            esperado = f"{reverse('login')}?next={reverse(nombre)}"
            self.assertRedirects(r, esperado, fetch_redirect_response=False)

    def test_logout_cierra_sesion(self):
        self.client.login(username="Oscar_QA", password="ClaveSegura#2026")
        r = self.client.post(reverse("logout"))
        self.assertRedirects(r, reverse("login"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)


class PerfilPorUsuarioTests(TestCase):
    def test_cada_usuario_ve_su_propio_perfil(self):
        crear_jugador("Jugador_Uno")
        crear_jugador("Jugador_Dos")

        self.client.login(username="Jugador_Uno", password="ClaveSegura#2026")
        r1 = self.client.get(reverse("home"))
        self.assertEqual(r1.context["perfil"].gamer_tag, "Jugador_Uno")
        self.client.logout()

        self.client.login(username="Jugador_Dos", password="ClaveSegura#2026")
        r2 = self.client.get(reverse("home"))
        self.assertEqual(r2.context["perfil"].gamer_tag, "Jugador_Dos")


class RachaTests(TestCase):
    def _perfil_con_ultima_conexion(self, dias_atras):
        usuario, perfil = crear_jugador(f"Racha_{dias_atras}")
        perfil.racha_actual = 4
        perfil.ultima_conexion = timezone.localdate() - timedelta(days=dias_atras)
        perfil.save()
        return usuario

    def test_primera_conexion_empieza_en_1(self):
        usuario, _ = crear_jugador("Primera_Vez")
        perfil = get_perfil_activo(SimpleNamespace(user=usuario))
        self.assertEqual(perfil.racha_actual, 1)

    def test_conexion_ayer_suma_un_dia(self):
        usuario = self._perfil_con_ultima_conexion(1)
        perfil = get_perfil_activo(SimpleNamespace(user=usuario))
        self.assertEqual(perfil.racha_actual, 5)

    def test_conexion_hoy_no_cambia_la_racha(self):
        usuario = self._perfil_con_ultima_conexion(0)
        perfil = get_perfil_activo(SimpleNamespace(user=usuario))
        self.assertEqual(perfil.racha_actual, 4)

    def test_saltar_dias_reinicia_la_racha(self):
        usuario = self._perfil_con_ultima_conexion(5)
        perfil = get_perfil_activo(SimpleNamespace(user=usuario))
        self.assertEqual(perfil.racha_actual, 1)

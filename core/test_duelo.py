from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import PerfilJugador, Pregunta

CLAVE = "ClaveSegura#2026"


class DueloBase(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(username="Duelista", password=CLAVE)
        self.perfil = PerfilJugador.objects.create(usuario=usuario, gamer_tag="Duelista")
        Pregunta.objects.create(
            categoria="Vocabulario",
            enunciado="¿Cómo se dice 'Desafío' en inglés?",
            opcion_a="Lesson",
            opcion_b="Challenge",
            opcion_c="Exam",
            opcion_d="Slow",
            respuesta_correcta="B",
        )
        self.client.login(username="Duelista", password=CLAVE)

    def abrir_duelo(self):
        return self.client.get(reverse("sala_duelo_directa"))

    def responder(self, opcion):
        return self.client.post(reverse("responder"), {"opcion": opcion})

    def perfil_actual(self):
        self.perfil.refresh_from_db()
        return self.perfil

    def envejecer_duelo(self, segundos):
        sesion = self.client.session
        duelo = sesion["duelo"]
        duelo["inicio"] -= segundos
        sesion["duelo"] = duelo
        sesion.save()


class DueloTests(DueloBase):
    def test_la_pagina_no_revela_la_respuesta(self):
        r = self.abrir_duelo()
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Challenge")
        self.assertNotContains(r, "respuestaCorrecta")
        html = r.content.decode()
        self.assertNotRegex(html, r"""=\s*["']B["']""")
        # "respuesta_correcta" solo puede aparecer como nombre del campo que devuelve el servidor
        self.assertNotIn("respuesta_correcta", html.replace("datos.respuesta_correcta", ""))

    def test_respuesta_correcta_suma_xp_y_victoria(self):
        self.abrir_duelo()
        r = self.responder("B")
        self.assertEqual(r.json()["estado"], "correcta")
        self.assertEqual(r.json()["xp_ganado"], 10)
        perfil = self.perfil_actual()
        self.assertEqual(perfil.puntos_xp, 10)
        self.assertEqual(perfil.victorias, 1)
        self.assertEqual(perfil.derrotas, 0)

    def test_respuesta_incorrecta_suma_derrota(self):
        self.abrir_duelo()
        r = self.responder("A")
        self.assertEqual(r.json()["estado"], "incorrecta")
        self.assertEqual(r.json()["respuesta_correcta"], "B")
        perfil = self.perfil_actual()
        self.assertEqual(perfil.puntos_xp, 0)
        self.assertEqual(perfil.derrotas, 1)

    def test_no_se_puede_responder_dos_veces(self):
        self.abrir_duelo()
        self.responder("B")
        r = self.responder("B")
        self.assertEqual(r.status_code, 400)
        perfil = self.perfil_actual()
        self.assertEqual(perfil.puntos_xp, 10)
        self.assertEqual(perfil.victorias, 1)

    def test_responder_sin_abrir_duelo_falla(self):
        r = self.responder("B")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(self.perfil_actual().puntos_xp, 0)

    def test_respuesta_tarde_cuenta_como_derrota(self):
        self.abrir_duelo()
        self.envejecer_duelo(100)
        r = self.responder("B")
        self.assertEqual(r.json()["estado"], "tiempo")
        perfil = self.perfil_actual()
        self.assertEqual(perfil.puntos_xp, 0)
        self.assertEqual(perfil.derrotas, 1)

    def test_tiempo_agotado_cuenta_como_derrota(self):
        self.abrir_duelo()
        r = self.responder("")
        self.assertEqual(r.json()["estado"], "tiempo")
        self.assertEqual(self.perfil_actual().derrotas, 1)

    def test_opcion_invalida_se_rechaza(self):
        self.abrir_duelo()
        r = self.responder("Z")
        self.assertEqual(r.status_code, 400)
        perfil = self.perfil_actual()
        self.assertEqual((perfil.puntos_xp, perfil.victorias, perfil.derrotas), (0, 0, 0))

    def test_exige_sesion(self):
        self.client.logout()
        r = self.responder("B")
        self.assertRedirects(
            r,
            f"{reverse('login')}?next={reverse('responder')}",
            fetch_redirect_response=False,
        )

    def test_solo_acepta_post(self):
        r = self.client.get(reverse("responder"))
        self.assertEqual(r.status_code, 405)

    def test_sin_preguntas_no_falla(self):
        Pregunta.objects.all().delete()
        r = self.abrir_duelo()
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Aún no hay preguntas")
        self.assertEqual(self.responder("A").status_code, 400)

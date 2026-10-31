
from django.test import TestCase
from django.contrib.auth.models import User
from verbattle.models import PerfilJugador, Pregunta


class VerbattlePruebasCalidad(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="Gamer_Estudiante",
            email="estudiante@leondegreiff.edu.co",
            password="Password123!"
        )

        self.perfil = PerfilJugador.objects.create(
            usuario=self.usuario,
            nivel_dominio="Medio",
            puntos_xp=1200
        )

        self.pregunta = Pregunta.objects.create(
            pregunta="¿Cómo se dice 'Duelo intelectual rápido' en inglés?",
            opcion_a="Challenge / Fast Duel",
            opcion_b="Static Lesson",
            opcion_c="Boring Exam",
            opcion_d="Slow Process",
            respuesta_correcta="A",
            categoria="Vocabulario Gamer"
        )

    def test_creacion_perfil_jugador(self):
        self.assertEqual(
            self.perfil.usuario.username,
            "Gamer_Estudiante"
        )
        self.assertEqual(self.perfil.nivel_dominio, "Medio")
        self.assertEqual(self.perfil.puntos_xp, 1200)

    def test_validacion_reto_linguistico(self):
        self.assertEqual(self.pregunta.respuesta_correcta, "A")
        self.assertNotEqual(
            self.pregunta.opcion_a,
            self.pregunta.opcion_b
        )

    def test_calculo_puntuacion_duelo(self):
        puntos_iniciales = self.perfil.puntos_xp

        self.perfil.puntos_xp += 150
        self.perfil.save()

        self.assertEqual(
            self.perfil.puntos_xp,
            puntos_iniciales + 150
        )

from django.test import TestCase
from django.contrib.auth.models import User
from verbattle.models import PerfilJugador, Pregunta


class VerbattlePruebasCalidad(TestCase):

    def setUp(self):
        """Configuración de datos de prueba iniciales para la ejecución"""

        # Crear usuario de prueba
        self.usuario = User.objects.create_user(
            username="Gamer_Estudiante",
            email="estudiante@leondegreiff.edu.co",
            password="Password123!"
        )

        # Perfil asignado
        self.perfil = PerfilJugador.objects.create(
            usuario=self.usuario,
            nivel_dominio="Medio",
            puntos=1200
        )

        # Pregunta / Reto de prueba
        self.pregunta = Pregunta.objects.create(
            enunciado="¿Cómo se dice 'Duelo intelectual rápido' en inglés?",
            opcion_a="Challenge / Fast Duel",
            opcion_b="Static Lesson",
            opcion_c="Boring Exam",
            opcion_d="Slow Process",
            respuesta_correcta="A",
            categoria="Vocabulario Gamer"
        )

    def test_creacion_perfil_jugador(self):
        """Prueba 1: Verificar que el perfil inicie con el nivel y puntos asignados"""

        self.assertEqual(self.perfil.usuario.username, "Gamer_Estudiante")
        self.assertEqual(self.perfil.nivel_dominio, "Medio")
        self.assertEqual(self.perfil.puntos, 1200)

    def test_validacion_reto_linguistico(self):
        """Prueba 2: Comprobar que la respuesta correcta del reto coincida con la opción A"""

        self.assertEqual(self.pregunta.respuesta_correcta, "A")
        self.assertNotEqual(self.pregunta.opcion_a, self.pregunta.opcion_b)

    def test_calculo_puntuacion_duelo(self):
        """Prueba 3: Simular ganancia de experiencia (+150 PTS) tras una victoria en la arena"""

        puntos_iniciales = self.perfil.puntos
        puntos_ganados = 150

        self.perfil.puntos += puntos_ganados
        self.perfil.save()

        self.assertEqual(
            self.perfil.puntos,
            puntos_iniciales + 150
        )
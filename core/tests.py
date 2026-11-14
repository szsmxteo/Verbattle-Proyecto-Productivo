from django.test import TestCase
from .models import Pregunta, PerfilJugador

class PreguntaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creamos una pregunta usando los campos EXACTOS de tu modelo
        Pregunta.objects.create(
            categoria="Vocabulario",
            enunciado="¿Cómo se dice 'Perro' en inglés?",
            opcion_a="Dog",
            opcion_b="Cat",
            opcion_c="Bird",
            opcion_d="Fish",
            respuesta_correcta="A"
        )

    def test_pregunta_creada_correctamente(self):
        # Obtenemos la pregunta de la base de datos temporal
        pregunta = Pregunta.objects.get(id=1)
        
        # Verificamos que los datos se guardaron bien
        self.assertEqual(pregunta.enunciado, "¿Cómo se dice 'Perro' en inglés?")
        self.assertEqual(pregunta.respuesta_correcta, "A")
        self.assertEqual(pregunta.opcion_a, "Dog")


class PerfilJugadorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creamos un perfil de prueba
        PerfilJugador.objects.create(
            gamer_tag="Oscar_QA",
            nivel_dominio="ALTO",
            puntos_xp=100
        )

    def test_perfil_creado_correctamente(self):
        jugador = PerfilJugador.objects.get(gamer_tag="Oscar_QA")
        
        # Verificamos sus datos iniciales
        self.assertEqual(jugador.puntos_xp, 100)
        self.assertEqual(jugador.nivel_dominio, "ALTO")
        self.assertEqual(jugador.racha_actual, 0) # Por defecto debe ser 0
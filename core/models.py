from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    nombre_completo = models.CharField(max_length=150)
    puntaje = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre_completo

class SalaVirtual(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    jugador_1 = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name="salas_como_jugador_1"
    )
    jugador_2 = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name="salas_como_jugador_2",
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class RetoLinguistico(models.Model):

    IDIOMAS = [
        ('EN', 'Inglés'),
        ('ES', 'Español'),
    ]

    sala = models.ForeignKey(
        SalaVirtual,
        on_delete=models.CASCADE,
        related_name="retos"
    )

    idioma = models.CharField(
        max_length=2,
        choices=IDIOMAS
    )

    pregunta = models.TextField()
    respuesta_correcta = models.CharField(max_length=255)
    dificultad = models.CharField(max_length=20, default="Fácil")
    puntos = models.IntegerField(default=10)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pregunta

class ProgresoRanking(models.Model):

    usuario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name="progresos"
    )

    reto = models.ForeignKey(
        RetoLinguistico,
        on_delete=models.CASCADE,
        related_name="resultados"
    )

    respuesta_usuario = models.CharField(max_length=255)
    correcta = models.BooleanField(default=False)
    puntos_obtenidos = models.IntegerField(default=0)

    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.puntos_obtenidos} puntos"
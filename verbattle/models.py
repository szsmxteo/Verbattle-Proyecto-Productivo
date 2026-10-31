from django.db import models
from django.contrib.auth.models import User

class PerfilJugador(models.Model):
    NIVELES = [
        ('BAJO', 'Bajo'),
        ('MEDIO', 'Medio'),
        ('ALTO', 'Alto'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gamer_tag = models.CharField(max_length=50, default="Gamer_Estudiante")
    nivel_dominio = models.CharField(max_length=10, choices=NIVELES, default='BAJO')
    puntos_xp = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.gamer_tag} ({self.puntos_xp} XP)"


class SalaVirtual(models.Model):
    ESTADOS = [
        ('ESPERANDO', 'Esperando Oponente'),
        ('EN_JUEGO', 'En Juego'),
        ('FINALIZADO', 'Finalizado'),
    ]

    codigo_sala = models.CharField(max_length=10, unique=True)
    jugador1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salas_creadas", null=True, blank=True)
    jugador2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salas_unidas", null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='ESPERANDO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sala #{self.codigo_sala} - {self.estado}"

# Alias de seguridad para evitar errores de importación
SalaDuelo = SalaVirtual


class Pregunta(models.Model):
    categoria = models.CharField(max_length=100, default="VOCABULARIO GAMER")
    pregunta = models.TextField()
    opcion_a = models.CharField(max_length=200)
    opcion_b = models.CharField(max_length=200)
    opcion_c = models.CharField(max_length=200)
    opcion_d = models.CharField(max_length=200)
    respuesta_correcta = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.pregunta[:50]
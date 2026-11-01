from django.db import models
from django.contrib.auth.models import User

class PerfilJugador(models.Model):
    # Vinculamos con el usuario de Django (opcional pero recomendado)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Campos según el Documento Maestro
    NIVELES = [('BAJO', 'Bajo'), ('MEDIO', 'Medio'), ('ALTO', 'Alto')]
    gamer_tag = models.CharField(max_length=50, default='Gamer_Estudiante')
    nivel_dominio = models.CharField(max_length=10, choices=NIVELES, default='BAJO')
    puntos_xp = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    
    # NUEVOS CAMPOS PARA EL SISTEMA DE RACHAS (Streak)
    racha_actual = models.IntegerField(default=0)
    ultima_conexion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.gamer_tag

class SalaVirtual(models.Model):
    codigo_sala = models.CharField(max_length=10, unique=True)
    estado = models.CharField(max_length=20, default='ESPERANDO') # ESPERANDO, JUGANDO, FINALIZADA
    jugador1 = models.ForeignKey(PerfilJugador, related_name='salas_anfitrion', on_delete=models.CASCADE)
    jugador2 = models.ForeignKey(PerfilJugador, related_name='salas_invitado', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sala {self.codigo_sala} - {self.estado}"

class Pregunta(models.Model):
    categoria = models.CharField(max_length=50)
    enunciado = models.TextField()
    opcion_a = models.CharField(max_length=100)
    opcion_b = models.CharField(max_length=100)
    opcion_c = models.CharField(max_length=100)
    opcion_d = models.CharField(max_length=100)
    respuesta_correcta = models.CharField(max_length=1)

    def __str__(self):
        return self.enunciado
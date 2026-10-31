from django.contrib import admin
from .models import PerfilJugador, SalaVirtual, Pregunta

# Registro de los modelos en el Panel de Administración de Django
admin.site.register(PerfilJugador)
admin.site.register(SalaVirtual)
admin.site.register(Pregunta)
from django.contrib import admin
from .models import PerfilJugador, SalaVirtual, Pregunta

# Registramos los 3 modelos oficiales del Documento Maestro
admin.site.register(PerfilJugador)
admin.site.register(SalaVirtual)
admin.site.register(Pregunta)
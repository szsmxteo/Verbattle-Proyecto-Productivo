from django.contrib import admin
from .models import (
    PerfilUsuario,
    SalaVirtual,
    RetoLinguistico,
    ProgresoRanking
)

admin.site.register(PerfilUsuario)
admin.site.register(SalaVirtual)
admin.site.register(RetoLinguistico)
admin.site.register(ProgresoRanking)
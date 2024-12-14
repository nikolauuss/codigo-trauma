from django.contrib import admin
from .models import Emergencia, RespuestaEmergencia

# Admin para el modelo Emergencia
@admin.register(Emergencia)
class EmergenciaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'num_victimas', 'ubicacion', 'fecha')
    search_fields = ('tipo', 'ubicacion')
    list_filter = ('tipo',)

# Admin para el modelo RespuestaEmergencia
@admin.register(RespuestaEmergencia)
class RespuestaEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('emergencia', 'miembro', 'ha_respondido', 'tiempo_respuesta')
    list_filter = ('ha_respondido',)
    search_fields = ('emergencia__tipo', 'miembro__username')


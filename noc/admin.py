from django.contrib import admin
from .models import NoConformidad


@admin.register(NoConformidad)
class NoConformidadAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'proyecto', 'responsable', 'estado', 'fecha_detectada', 'fecha_cierre')
    list_filter = ('estado', 'proyecto')
    search_fields = ('codigo', 'descripcion', 'accion_correctiva')
    date_hierarchy = 'fecha_detectada'

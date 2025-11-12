from django.contrib import admin
from .models import Actividad


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'descripcion', 'responsable', 'fecha_programada', 'fecha_real', 'estado', 'avance')
    list_filter = ('estado', 'proyecto')
    search_fields = ('descripcion',)
    list_editable = ('estado', 'avance')
    ordering = ('proyecto', 'fecha_programada')

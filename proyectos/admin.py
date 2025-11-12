from django.contrib import admin
from .models import Proyecto, CuadroControl
from actividades.models import Actividad
from noc.models import NoConformidad


class ActividadInline(admin.TabularInline):
    model = Actividad
    extra = 1
    fields = ('item', 'descripcion', 'responsable', 'fecha_programada', 'fecha_real', 'avance', 'estado')
    classes = ['collapse']
    show_change_link = True


class NoConformidadInline(admin.TabularInline):
    model = NoConformidad
    extra = 0
    fields = ('codigo', 'descripcion', 'responsable', 'estado', 'fecha_detectada', 'fecha_cierre')
    readonly_fields = ('codigo',)
    classes = ['collapse']
    show_change_link = True


class CuadroControlInline(admin.StackedInline):
    model = CuadroControl
    extra = 0
    fields = ('total_actividades', 'completadas', 'avance_global', 'fecha_actualizacion')
    readonly_fields = ('total_actividades', 'completadas', 'avance_global', 'fecha_actualizacion')
    can_delete = False


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'cliente', 'responsable', 'estado', 'fecha_inicio', 'fecha_termino')
    list_filter = ('estado', 'cliente')
    search_fields = ('codigo', 'nombre')
    date_hierarchy = 'fecha_inicio'
    inlines = [CuadroControlInline, ActividadInline, NoConformidadInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'cliente')
        }),
        ('Responsables', {
            'fields': ('responsable', 'supervisor')
        }),
        ('Fechas y Estado', {
            'fields': ('fecha_inicio', 'fecha_termino', 'estado')
        }),
    )


@admin.register(CuadroControl)
class CuadroControlAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'total_actividades', 'completadas', 'avance_global', 'fecha_actualizacion')
    readonly_fields = ('total_actividades', 'completadas', 'avance_global', 'fecha_actualizacion')
    
    fieldsets = (
        ('Proyecto', {
            'fields': ('proyecto',)
        }),
        ('Estadísticas', {
            'fields': ('total_actividades', 'completadas', 'avance_global')
        }),
        ('Actualización', {
            'fields': ('fecha_actualizacion',)
        }),
    )

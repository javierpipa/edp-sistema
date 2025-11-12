from django.contrib import admin
from .models import Empresa
from proyectos.models import Proyecto


class ProyectoInline(admin.TabularInline):
    model = Proyecto
    extra = 0
    fields = ('codigo', 'nombre', 'responsable', 'estado', 'fecha_inicio')
    readonly_fields = ('codigo',)
    can_delete = False
    show_change_link = True


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'contacto', 'correo')
    search_fields = ('nombre', 'rut')
    list_filter = ('nombre',)
    inlines = [ProyectoInline]

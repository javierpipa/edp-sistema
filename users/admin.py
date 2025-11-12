from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from proyectos.models import Proyecto
from actividades.models import Actividad


class ProyectoResponsableInline(admin.TabularInline):
    model = Proyecto
    fk_name = 'responsable'
    extra = 0
    fields = ('codigo', 'nombre', 'cliente', 'estado', 'fecha_inicio')
    readonly_fields = ('codigo', 'nombre', 'cliente')
    can_delete = False
    show_change_link = True
    verbose_name = 'Proyecto como Responsable'
    verbose_name_plural = 'Proyectos como Responsable'


class ActividadAsignadaInline(admin.TabularInline):
    model = Actividad
    fk_name = 'responsable'
    extra = 0
    fields = ('proyecto', 'item', 'descripcion', 'estado', 'avance', 'fecha_programada')
    readonly_fields = ('proyecto', 'item', 'descripcion')
    can_delete = False
    show_change_link = True
    verbose_name = 'Actividad Asignada'
    verbose_name_plural = 'Actividades Asignadas'
    classes = ['collapse']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    inlines = [ProyectoResponsableInline, ActividadAsignadaInline]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': (),
            'description': 'Ver proyectos y actividades asignadas en las secciones inferiores.'
        }),
    )

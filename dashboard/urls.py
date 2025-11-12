from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # Proyectos
    path('proyectos/', views.proyectos_lista, name='proyectos_lista'),
    path('proyectos/crear/', views.proyecto_crear, name='proyecto_crear'),
    path('proyectos/<int:proyecto_id>/', views.proyecto_detalle, name='proyecto_detalle'),
    path('proyectos/<int:proyecto_id>/editar/', views.proyecto_editar, name='proyecto_editar'),
    path('proyectos/<int:proyecto_id>/eliminar/', views.proyecto_eliminar, name='proyecto_eliminar'),
    
    # Actividades
    path('actividades/', views.actividades_lista, name='actividades_lista'),
    path('actividades/crear/', views.actividad_crear, name='actividad_crear'),
    path('actividades/crear/<int:proyecto_id>/', views.actividad_crear, name='actividad_crear_proyecto'),
    path('actividades/<int:actividad_id>/editar/', views.actividad_editar, name='actividad_editar'),
    path('actividades/<int:actividad_id>/eliminar/', views.actividad_eliminar, name='actividad_eliminar'),
    
    # Empresas
    path('empresas/', views.empresas_lista, name='empresas_lista'),
    path('empresas/crear/', views.empresa_crear, name='empresa_crear'),
    path('empresas/<int:empresa_id>/editar/', views.empresa_editar, name='empresa_editar'),
    path('empresas/<int:empresa_id>/eliminar/', views.empresa_eliminar, name='empresa_eliminar'),
    
    # NOC (No Conformidades)
    path('noc/crear/', views.noc_crear, name='noc_crear'),
    path('noc/crear/<int:proyecto_id>/', views.noc_crear, name='noc_crear_proyecto'),
    path('noc/<int:noc_id>/editar/', views.noc_editar, name='noc_editar'),
    path('noc/<int:noc_id>/eliminar/', views.noc_eliminar, name='noc_eliminar'),
]

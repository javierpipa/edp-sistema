from django.urls import path
from .views import dashboard, proyectos_lista, proyecto_detalle, actividades_lista

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('proyectos/', proyectos_lista, name='proyectos_lista'),
    path('proyectos/<int:proyecto_id>/', proyecto_detalle, name='proyecto_detalle'),
    path('actividades/', actividades_lista, name='actividades_lista'),
]

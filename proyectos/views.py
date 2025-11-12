from rest_framework import viewsets
from .models import Proyecto, CuadroControl
from .serializers import ProyectoSerializer, CuadroControlSerializer


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


class CuadroControlViewSet(viewsets.ModelViewSet):
    queryset = CuadroControl.objects.all()
    serializer_class = CuadroControlSerializer

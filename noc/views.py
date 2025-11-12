from rest_framework import viewsets
from .models import NoConformidad
from .serializers import NoConformidadSerializer


class NoConformidadViewSet(viewsets.ModelViewSet):
    queryset = NoConformidad.objects.all()
    serializer_class = NoConformidadSerializer

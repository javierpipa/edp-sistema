from rest_framework import serializers
from .models import Actividad
from users.serializers import UsuarioSerializer


class ActividadSerializer(serializers.ModelSerializer):
    responsable = UsuarioSerializer(read_only=True)
    proyecto = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Actividad
        fields = '__all__'

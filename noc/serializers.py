from rest_framework import serializers
from .models import NoConformidad
from users.serializers import UsuarioSerializer


class NoConformidadSerializer(serializers.ModelSerializer):
    responsable = UsuarioSerializer(read_only=True)
    proyecto = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NoConformidad
        fields = '__all__'

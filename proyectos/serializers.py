from rest_framework import serializers
from .models import Proyecto, CuadroControl
from empresas.serializers import EmpresaSerializer
from users.serializers import UsuarioSerializer


class ProyectoSerializer(serializers.ModelSerializer):
    cliente = EmpresaSerializer(read_only=True)
    responsable = UsuarioSerializer(read_only=True)
    avance_global = serializers.SerializerMethodField()

    class Meta:
        model = Proyecto
        fields = [
            'id', 'codigo', 'nombre', 'cliente', 'responsable', 'supervisor',
            'fecha_inicio', 'fecha_termino', 'estado', 'avance_global'
        ]

    def get_avance_global(self, obj: Proyecto) -> float:
        control = getattr(obj, 'control', None)
        return float(control.avance_global) if control else 0.0


class CuadroControlSerializer(serializers.ModelSerializer):
    proyecto = ProyectoSerializer(read_only=True)

    class Meta:
        model = CuadroControl
        fields = '__all__'

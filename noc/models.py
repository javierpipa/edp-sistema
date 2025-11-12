from django.db import models
from django.conf import settings
from proyectos.models import Proyecto


class NoConformidad(models.Model):
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('cerrada', 'Cerrada')
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='noc')
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField()
    causa = models.TextField(blank=True, null=True)
    accion_correctiva = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='noc_responsables'
    )
    fecha_detectada = models.DateField()
    fecha_cierre = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='abierta'
    )

    class Meta:
        verbose_name = "No Conformidad"
        verbose_name_plural = "No Conformidades"
        ordering = ['-fecha_detectada']

    def __str__(self) -> str:
        return f"NOC {self.codigo} - {self.proyecto.codigo}"

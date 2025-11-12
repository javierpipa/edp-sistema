from django.db import models
from django.conf import settings
from proyectos.models import Proyecto


class Actividad(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_ejecucion', 'En Ejecución'),
        ('completada', 'Completada'),
        ('atrasada', 'Atrasada')
    ]

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='actividades')
    item = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField()
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='actividades_asignadas'
    )
    fecha_programada = models.DateField(blank=True, null=True)
    fecha_real = models.DateField(blank=True, null=True)
    avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['proyecto', 'fecha_programada']

    def __str__(self) -> str:
        return f"{self.proyecto.codigo} - {self.descripcion[:50]}"

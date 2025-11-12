from django.db import models
from django.conf import settings
from empresas.models import Empresa


class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('planificado', 'Planificado'),
        ('en_ejecucion', 'En Ejecución'),
        ('finalizado', 'Finalizado'),
        ('suspendido', 'Suspendido')
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    cliente = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='proyectos')
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='proyectos_responsables'
    )
    supervisor = models.CharField(max_length=200, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_CHOICES,
        default='planificado'
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_inicio']

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class CuadroControl(models.Model):
    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE, related_name='control')
    total_actividades = models.PositiveIntegerField(default=0)
    completadas = models.PositiveIntegerField(default=0)
    avance_global = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cuadro de Control"
        verbose_name_plural = "Cuadros de Control"

    def actualizar(self) -> None:
        """Actualiza el avance global del proyecto basado en las actividades."""
        total = self.proyecto.actividades.count()
        completadas = self.proyecto.actividades.filter(estado='completada').count()
        avance = (completadas / total * 100) if total else 0
        self.total_actividades = total
        self.completadas = completadas
        self.avance_global = avance
        self.save()

    def __str__(self) -> str:
        return f"Control {self.proyecto.codigo} ({self.avance_global}%)"

from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, blank=True, null=True)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre

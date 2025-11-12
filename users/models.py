from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model. Aunque no se personaliza ahora,
    es mejor práctica definirlo desde el inicio.
    """
    pass

    def __str__(self) -> str:
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def is_in_group(self, group_name):
        """
        Verifica si el usuario pertenece al grupo especificado.
        """
        return self.groups.filter(name=group_name).exists()

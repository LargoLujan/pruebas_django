from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def is_in_group(self, group_name):
        """
        Verifica si el usuario pertenece al grupo especificado.
        """
        return self.groups.filter(name=group_name).exists()


# Modelo de noticia
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

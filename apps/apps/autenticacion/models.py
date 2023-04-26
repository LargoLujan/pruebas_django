from django.contrib.auth import get_user_model
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


class CalendarioLaboral(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha = models.DateField()
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    dia_libre = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.fecha}"


class Evento(models.Model):
    TIPOS = (
        ('vacaciones', 'Vacaciones'),
        ('festivo', 'Día festivo'),
        ('festivo_trabaja', 'Día festivo trabaja'),
        ('horario', 'Horario laboral'),
        ('libranza', 'Libranza'),
        ('baja_medica', 'Baja médica'),
        ('baja_maternal', 'Baja maternal/Paternal'),
        ('ausencia', 'Ausencia'),

    )

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.titulo

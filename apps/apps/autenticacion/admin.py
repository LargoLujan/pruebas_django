from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Evento, Noticia, CalendarioLaboral  # Asegúrate de importar tu modelo de usuario personalizado

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Noticia)
admin.site.register(CalendarioLaboral)
admin.site.register(Evento)

# Register your models here.

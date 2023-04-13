from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Asegúrate de importar tu modelo de usuario personalizado

admin.site.register(CustomUser, UserAdmin)


# Register your models here.

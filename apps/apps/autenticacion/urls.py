from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.ingresar, name='login'),
    path('contenido/', views.contenido, name='contenido'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/editar/', views.update_profile, name='update_profile'),
    path('perfil/', views.perfil, name='perfil'),
    path('administracion_panel/', views.administracion_panel, name='administracion_panel'),
    path('estructura_panel/', views.estructura_panel, name='estructura_panel'),
    path('hr_panel/', views.hr_panel, name='hr_panel'),
    path('sin_grupo/', views.administracion_panel, name='sin_grupo'),
]

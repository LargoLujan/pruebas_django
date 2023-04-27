from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Noticia, Evento



class UpdateProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False, help_text='Opcional. Sube una nueva imagen de perfil.')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'image', 'password')
        readonly_fields = ('password',)

    def clean_password(self):
        return self.initial['password']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Obligatorio.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Obligatorio.')
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Obligatorio. Ingrese un correo electrónico válido.')
    image = forms.ImageField(required=False, help_text='Opcional. Sube una imagen de perfil.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'password1', 'password2')


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'autor', 'imagen', 'enlace']
        exclude = ['fecha_publicacion']  # Excluye el campo fecha_publicación


class AgregarEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'color']


class EventoForm(forms.ModelForm):
    COLOR_CHOICES = [
        ('#FF0000', 'Rojo'),
        ('#00FF00', 'Verde'),
        ('#0000FF', 'Azul'),
        ('#FFFF00', 'Amarillo'),
        ('#FFA500', 'Naranja'),
    ]

    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select)

    class Meta:
        model = Evento
        fields = ['titulo', 'fecha_inicio', 'fecha_fin', 'color']
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

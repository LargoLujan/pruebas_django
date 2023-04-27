from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Noticia, Evento
from .helpers import get_users_with_group
from django.forms.widgets import SelectMultiple


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


class GroupSelectMultiple(SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        option['attrs']['class'] = 'option-group'
        return option


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.username} ({obj.groups.first().name})" if obj.groups.exists() else obj.username


class EventoForm(forms.ModelForm):
    COLOR_CHOICES = [
        ('#FF0000', 'Rojo'),
        ('#00FF00', 'Verde'),
        ('#0000FF', 'Azul'),
        ('#FFFF00', 'Amarillo'),
        ('#FFA500', 'Naranja'),
    ]

    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select)

    usuarios_autorizados = CustomModelMultipleChoiceField(
        queryset=get_users_with_group(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'fecha_inicio', 'fecha_fin', 'color', 'usuarios_autorizados']
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

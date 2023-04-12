from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UpdateProfileForm, CustomUserCreationForm


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('contenido')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})


def ingresar(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('contenido')
        else:
            messages.error(request, 'Error en el inicio de sesión. Por favor, revisa tus credenciales.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def contenido(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'contenido.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('login')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'autenticacion/update_profile.html', {'form': form})


@login_required
def perfil(request):
    user = request.user
    context = {
        'user': user,
        'photo': user.image,  # obtener la foto del usuario
    }
    return render(request, 'autenticacion/perfil.html', context)
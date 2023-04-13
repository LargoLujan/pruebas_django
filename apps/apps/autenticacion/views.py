from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UpdateProfileForm, CustomUserCreationForm
from .utils import is_administrator, is_estructura, is_hr, is_estandar


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

            # Verificar si el usuario pertenece al grupo de administradores
            if request.user.groups.filter(name='admin').exists():
                return redirect('administracion_panel')
            elif request.user.groups.filter(name='staff').exists():
                return redirect('estructura')
            elif request.user.groups.filter(name='hr').exists():
                return redirect('hr_panel')
            elif request.user.groups.filter(name='estandar').exists():
                return redirect('contenido')
            else:
                return redirect('sin_grupo')

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
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UpdateProfileForm(instance=request.user)
    context = {
        'form': form,
        'image': request.user.image,  # agregar la imagen del usuario
    }
    return render(request, 'autenticacion/update_profile.html', context)


@login_required
def perfil(request):
    user = request.user
    context = {
        'user': user,
        'photo': user.image,  # obtener la foto del usuario
    }
    return render(request, 'autenticacion/perfil.html', context)


@user_passes_test(is_administrator)
def administracion_panel(request):
    return render(request, 'administracion_panel.html')


@user_passes_test(is_estructura)
def estructural(request):
    return render(request, 'estructura.html')


@user_passes_test(is_hr)
def hr_panel(request):
    return render(request, 'hr_panel.html')


@user_passes_test(is_estandar)
def estandar(request):
    return render(request, 'estandar.html')

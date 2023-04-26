from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from .forms import UpdateProfileForm, CustomUserCreationForm, NoticiaForm, EventoForm
from .models import Noticia, CalendarioLaboral, Evento
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
                return redirect('estructura_panel')
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
    return render(request, 'noticias.html')


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
    return render(request, 'admin/administracion_panel.html')


@user_passes_test(is_estructura)
def estructura_panel(request):
    return render(request, 'staff/estructura_panel.html')


@user_passes_test(is_hr)
def hr_panel(request):
    return render(request, 'hr/hr_panel.html')


@user_passes_test(is_estandar)
def estandar_panel(request):
    return render(request, 'noticias.html')


# Vista de lista de noticias
@user_passes_test(is_estandar)
def noticias(request):
    noticias = Noticia.objects.all()
    context = {'noticias': noticias}
    return render(request, 'noticias.html', context)


# Vista de creación de noticias
@login_required
@user_passes_test(is_estructura)
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect(reverse('noticias'))
    else:
        form = NoticiaForm()

    context = {'form': form}
    return render(request, 'crear_noticia.html', context)


@user_passes_test(is_estructura)
def editar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('noticias')
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'editar_noticia.html', {'form': form})


@user_passes_test(is_estructura)
def eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        return redirect('noticias')
    return render(request, 'eliminar_noticia.html', {'noticia': noticia})


def calendario(request):
    eventos = Evento.objects.all()

    events = []
    for evento in eventos:
        event = {
            'title': evento.titulo,
            'start': evento.fecha_inicio.isoformat(),
            'color': evento.color
        }
        if evento.fecha_fin:
            event['end'] = evento.fecha_fin.isoformat()

        events.append(event)

    context = {'events': events}
    return render(request, 'calendario.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='hr').exists())
def evento_form(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()
            messages.success(request, 'El evento ha sido creado con éxito.')
            return redirect('hr_panel')
    else:
        form = EventoForm()
    return render(request, 'hr/evento_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='hr').exists())
def evento_create(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.autor = request.user
            evento.save()
            return redirect('hr_panel')
    else:
        form = NoticiaForm()

    context = {'form': form}
    return render(request, 'hr/evento_form.html', context)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='hr').exists())
def evento_update(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('hr_panel')
    else:
        form = NoticiaForm(instance=evento)
    context = {'form': form}
    return render(request, 'hr/evento_form.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='hr').exists())
def evento_delete(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
        return redirect('hr_panel')
    context = {'evento': evento}
    return render(request, 'hr/evento_confirm_delete.html', context)




@login_required
@user_passes_test(is_hr)
def planificacion(request):
    return render(request, 'hr/planificacion.html')

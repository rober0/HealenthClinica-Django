from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Paciente, Medico, Administrador
from users.decorators import admin_required, medico_required, paciente_required
from django.contrib import messages
from django.contrib.auth import login
from users.models import Usuario, Paciente, Medico, Administrador
from dashboard.forms import PacienteForm, MedicoForm, AdministradorForm
from django.contrib.auth import update_session_auth_hash, get_user_model

def edit_user(request, user_id):
    user = Usuario.objects.get(pk=user_id)
    if hasattr(user, 'paciente'):
        instance = user.paciente
        form_class = PacienteForm
    elif hasattr(user, 'medico'):
        instance = user.medico
        form_class = MedicoForm
    elif hasattr(user, 'administrador'):
        instance = user.administrador
        form_class = AdministradorForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('dashboard:administrador_listas')
    else:
        form = form_class(instance=instance)

    return render(request, 'dashboard/administradores/lista/edit.html', {'form': form, 'edit_user': user})

def view_config(request):
    user = request.user
    if hasattr(user, 'paciente'):
        instance = user.paciente
        form_class = PacienteForm
        template = 'dashboard/pacientes/settings.html'
    elif hasattr(user, 'medico'):
        instance = user.medico
        form_class = MedicoForm
        template = 'dashboard/medicos/settings.html'
    elif hasattr(user, 'administrador'):
        instance = user.administrador
        form_class = AdministradorForm
        template = 'dashboard/administradores/settings.html'
    else:
        return redirect('users:login')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            request.user.refresh_from_db()
            update_session_auth_hash(request, request.user)
           
            if hasattr(user, 'paciente'):
                return redirect('dashboard:pacientes')
            elif hasattr(user, 'medico'):
                return redirect('dashboard:medicos')
            elif hasattr(user, 'administrador'):
                return redirect('dashboard:administrador')
    else:
        form = form_class(instance=instance)

    return render(request, template, {'form': form, 'view_config': user})

def delete_user(request, user_id):
    user = Usuario.objects.get(pk=user_id)
    if hasattr(user, 'paciente'):
        user.paciente.delete()
    elif hasattr(user, 'medico'):
        user.medico.delete()
    elif hasattr(user, 'administrador'):
        user.administrador.delete()
    return redirect('dashboard:administrador_listas')

def register_pac(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.save()
            return redirect('dashboard:administrador_listas')
    else:
        form = PacienteForm()
    return render(request, 'dashboard/administradores/lista/regpac.html', {'form': form})

def register_med(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST, request.FILES)
        if form.is_valid():
            medico = form.save()
            return redirect('dashboard:administrador_listas')
    else:
        form = MedicoForm()
    return render(request, 'dashboard/administradores/lista/regmed.html', {'form': form})

def register_adm(request):
    if request.method == 'POST':
        form = AdministradorForm(request.POST, request.FILES)
        if form.is_valid():
            administrador = form.save()
            return redirect('dashboard:administrador_listas')
    else:
        form = AdministradorForm()
    return render(request, 'dashboard/administradores/lista/regadm.html', {'form': form})

@login_required(login_url='users:login')
def dashboard_view(request):
    if isinstance(request.user, Administrador):
        return redirect('dashboard:administrador')
    elif isinstance(request.user, Medico):
        return redirect('dashboard:medicos')
    elif isinstance(request.user, Paciente):
        return redirect('dashboard:pacientes')
    return redirect('users:login')

@login_required(login_url='users:login')
@admin_required
def administrador(request):
    return render(request, 'dashboard/administradores/dashboard.html')

@login_required(login_url='users:login')
@admin_required
def administrador_agendamentos(request):
    return render(request, 'dashboard/administradores/agendamentos.html')

@login_required(login_url='users:login')
@admin_required
def administrador_lista(request):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    administradores = Administrador.objects.all()
    
    context = {
        'pacientes': pacientes,
        'medicos': medicos,
        'administradores': administradores,
    }
    return render(request, 'dashboard/administradores/listas.html', context)

@login_required(login_url='users:login')
@medico_required
def medico(request):
    return render(request, 'dashboard/medicos/dashboard.html')

@login_required(login_url='users:login')
@paciente_required
def paciente(request):
    return render(request, 'dashboard/pacientes/dashboard.html')

@login_required(login_url='users:login')
@paciente_required
def paciente_agenda(request):
    return render(request, 'dashboard/pacientes/agendamento.html')
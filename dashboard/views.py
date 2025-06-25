from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Paciente, Medico, Administrador
from users.decorators import admin_required, medico_required, paciente_required
from django.contrib import messages
from django.contrib.auth import login
from users.models import Usuario, Paciente, Medico, Administrador
from .forms import PacienteForm, MedicoForm, AdministradorForm

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
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('dashboard:administrador_listas')
    else:
        form = form_class(instance=instance)

    return render(request, 'dashboard/edit.html', {'form': form, 'user': user})

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
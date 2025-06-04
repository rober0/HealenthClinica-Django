from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import user_redirect_handler
from django.contrib.auth.decorators import user_passes_test
from users.models import Usuario

@login_required(login_url='users:login')
@user_redirect_handler
def pacientes(request):
    return render(request, 'dashboard/dashboardpac.html')

@login_required(login_url='users:login')
@user_redirect_handler
def pacientes_agenda(request):
    return render(request, 'dashboard/agendamentopac.html')

@login_required(login_url='users:login')
@user_redirect_handler
def pacientes_agendamedico(request):
    return render(request, 'dashboard/agendamentopacmed.html')

@login_required(login_url='users:login')
def medicos(request):
    return render(request, 'dashboard/dashboardmed.html')

@login_required(login_url='users:login')
def medicos_agenda(request):
    return render(request, 'dashboard/agendamentomed.html')

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required(login_url='users:login')
@user_passes_test(is_admin, login_url='users:login')
def administrador(request):
    return render(request, 'dashboard/dashboardadm.html')

@login_required(login_url='users:login')
@user_passes_test(is_admin, login_url='users:login')
def administrador_agendamentos(request):
    return render(request, 'dashboard/agendamentosadm.html')

@login_required(login_url='users:login')
@user_passes_test(is_admin, login_url='users:login')
def administrador_lista(request):
    pacientes = Usuario.objects.filter(groups__name='Paciente')
    medicos = Usuario.objects.filter(groups__name='Medico')
    administradores = Usuario.objects.filter(groups__name='Admin')
    usuarios = Usuario.objects.all()
    context = {
        'pacientes': pacientes,
        'medicos': medicos,
        'admin': administradores,
        'usuarios': usuarios,
    }

    return render(request, 'dashboard/listasadm.html', context)

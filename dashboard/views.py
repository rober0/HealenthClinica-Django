from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import user_redirect_handler
from django.contrib.auth.decorators import user_passes_test

@login_required(login_url='users:login')
def pacientes(request):
    return render(request, 'dashboard/dashboardpac.html')

@login_required(login_url='users:login')
@user_redirect_handler
def pacientes_agenda(request):
    return render(request, 'dashboard/agendamentopac.html')

@login_required(login_url='users:login')
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
def administrador_medicos(request):
    return render(request, 'dashboard/medicosadm.html')

@login_required(login_url='users:login')
def administrador_pacientes(request):
    return render(request, 'dashboard/pacientesadm.html')

@login_required(login_url='users:login')
def administrador_medicos_agendamentos(request):
    return render(request, 'dashboard/agendamentosmedadm.html')

@login_required(login_url='users:login')
def administrador_pacientes_agendamentos(request):
    return render(request, 'dashboard/agendamentospacad.html')

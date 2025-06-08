from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Paciente, Medico, Administrador
from users.decorators import admin_required, medico_required, paciente_required

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
    return render(request, 'dashboard/dashboardadm.html')

@login_required(login_url='users:login')
@admin_required
def administrador_agendamentos(request):
    return render(request, 'dashboard/agendamentosadm.html')

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
    return render(request, 'dashboard/listasadm.html', context)

@login_required(login_url='users:login')
@medico_required
def medico(request):
    return render(request, 'dashboard/dashboardmed.html')

@login_required(login_url='users:login')
@paciente_required
def paciente(request):
    return render(request, 'dashboard/dashboardpac.html')
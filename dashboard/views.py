from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Usuario, Paciente, Medico, Administrador
from users.decorators import admin_required, medico_required, paciente_required
from dashboard.forms import PacienteForm, MedicoForm, AdministradorForm, AgendamentoForm
from dashboard.models import CriarEvento
import json

@login_required
@admin_required
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
    else:
        return redirect('dashboard:administrador_listas')

    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('dashboard:administrador_listas')
    else:
        form = form_class(instance=instance)

    return render(request, 'dashboard/administradores/lista/edit.html', {'form': form, 'edit_user': user})

@login_required
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
            update_session_auth_hash(request, request.user)

        if hasattr(user, 'paciente'):
            return redirect('dashboard:pacientes')
        elif hasattr(user, 'medico'):
            return redirect('dashboard:medicos')
        elif hasattr(user, 'administrador'):
            return redirect('dashboard:administrador')
        else:
            pass
    else:
        form = form_class(instance=instance)

        return render(request, template, {'form': form, 'view_config': user})

@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if hasattr(user, 'paciente'):
        user.paciente.delete()
    elif hasattr(user, 'medico'):
        user.medico.delete()
    elif hasattr(user, 'administrador'):
        user.administrador.delete()
    return redirect('dashboard:administrador_listas')

@login_required
@admin_required
def register_pac(request):
    form = PacienteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:administrador_listas')
    return render(request, 'dashboard/administradores/lista/regpac.html', {'form': form})

@login_required
@admin_required
def register_med(request):
    form = MedicoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:administrador_listas')
    return render(request, 'dashboard/administradores/lista/regmed.html', {'form': form})

@login_required
@admin_required
def register_adm(request):
    form = AdministradorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:administrador_listas')
    return render(request, 'dashboard/administradores/lista/regadm.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    if hasattr(user, 'administrador'):
        return redirect('dashboard:administrador')
    elif hasattr(user, 'medico'):
        return redirect('dashboard:medico')
    elif hasattr(user, 'paciente'):
        return redirect('dashboard:paciente')
    return redirect('users:login')

@login_required
@admin_required
def administrador(request):
    eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
    eventos_andamento = eventos.filter(data_inicio__lte=timezone.now(), data_fim__gte=timezone.now())
    eventos_completos = eventos.filter(data_fim__lt=timezone.now())
    eventos_proximos = eventos.filter(data_inicio__gte=timezone.now())
    eventos_cancelados = CriarEvento.objects.filter(is_active=False, is_deleted=True)

    context = {
        "eventos_andamento": eventos_andamento,
        "eventos_completos": eventos_completos,
        "eventos_proximos": eventos_proximos,
        "eventos_cancelados": eventos_cancelados,
        "proxima_data": eventos_proximos.first().data_inicio if eventos_proximos.exists() else None,
    }
    return render(request, 'dashboard/administradores/dashboard.html', context)

@login_required
@admin_required
def administrador_agendamentos(request):
    eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
    eventos_andamento = eventos.filter(data_inicio__lte=timezone.now(), data_fim__gte=timezone.now())
    eventos_completos = eventos.filter(data_fim__lt=timezone.now())
    eventos_proximos = eventos.filter(data_inicio__gte=timezone.now())
    ultimos_eventos = eventos.order_by("-id")[:10]

    event_list = [{
        "id": e.id,
        "paciente": e.paciente.username,
        "procedimentos": e.procedimentos,
        "convenio": e.convenio,
        "observacoes": e.observacoes,
        "start": e.data_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": e.data_fim.strftime("%Y-%m-%dT%H:%M:%S"),
    } for e in eventos]

    context = {
        "form": AgendamentoForm(),
        "ultimos_eventos": ultimos_eventos,
        "eventos_andamento": eventos_andamento,
        "eventos_completos": eventos_completos.count(),
        "eventos_proximos": eventos_proximos.count(),
        "eventos": json.dumps(event_list),
    }
    return render(request, "dashboard/administradores/agendamentos.html", context)

@login_required
@admin_required
def administrador_lista(request):
    context = {
        'pacientes': Paciente.objects.all(),
        'medicos': Medico.objects.all(),
        'administradores': Administrador.objects.all(),
    }
    return render(request, 'dashboard/administradores/listas.html', context)

@login_required
@medico_required
def medico(request):
    return render(request, 'dashboard/medicos/dashboard.html')

@login_required
@paciente_required
def paciente(request):
    return render(request, 'dashboard/pacientes/dashboard.html')

@login_required
@paciente_required
def paciente_agenda(request):
    return render(request, 'dashboard/pacientes/agendamento.html')

class CalendarView(LoginRequiredMixin, generic.View):
    login_url = "users:login"
    template_name = "dashboard/administradores/agendamentos.html"

    def get(self, request):
        eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
        event_list = [{
            "id": e.id,
            "paciente": e.paciente.username,
            "procedimentos": e.procedimentos,
            "convenio": e.convenio,
            "observacoes": e.observacoes,
            "start": e.data_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": e.data_fim.strftime("%Y-%m-%dT%H:%M:%S"),
        } for e in eventos]

        ultimos_eventos = eventos.order_by("-id")[:10]

        return render(request, self.template_name, {
            "form": AgendamentoForm(),
            "eventos": json.dumps(event_list),
            "ultimos_eventos": ultimos_eventos,
        })

@login_required
def create_agendamento(request):
    form = AgendamentoForm(request.POST or None)
    if form.is_valid():
        evento = form.save(commit=False)
        evento.usuario = request.user
        evento.save()
        return redirect("dashboard:calendar")
    return render(request, "dashboard/administradores/lista/evento.html", {"form": form})

@login_required
def delete_agendamento(request, event_id):
    eventos = get_object_or_404(CriarEvento, id=event_id)
    if request.method == 'POST':
        eventos.delete()
        return JsonResponse({'message': 'Agendamento deletado com sucesso.'})
    return JsonResponse({'message': 'Erro!'}, status=400)
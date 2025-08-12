from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from zoneinfo import ZoneInfo
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
    if hasattr(user, "paciente"):
        instance = user.paciente
        form_class = PacienteForm
    elif hasattr(user, "medico"):
        instance = user.medico
        form_class = MedicoForm
    elif hasattr(user, "administrador"):
        instance = user.administrador
        form_class = AdministradorForm
    else:
        return redirect("dashboard:administrador_listas")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return redirect("dashboard:administrador_listas")
    else:
        form = form_class(instance=instance)

    return render(
        request,
        "dashboard/administradores/lista/edit.html",
        {"form": form, "edit_user": user},
    )


@login_required
def view_config(request):
    user = request.user
    if hasattr(user, "paciente"):
        instance = user.paciente
        form_class = PacienteForm
        template = "dashboard/pacientes/settings.html"
    elif hasattr(user, "medico"):
        instance = user.medico
        form_class = MedicoForm
        template = "dashboard/medicos/settings.html"
    elif hasattr(user, "administrador"):
        instance = user.administrador
        form_class = AdministradorForm
        template = "dashboard/administradores/settings.html"
    else:
        return redirect("users:login")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            request.user.refresh_from_db()
            update_session_auth_hash(request, request.user)

        if hasattr(user, "paciente"):
            return redirect("dashboard:pacientes")
        elif hasattr(user, "medico"):
            return redirect("dashboard:medicos")
        elif hasattr(user, "administrador"):
            return redirect("dashboard:administrador")
        else:
            pass
    else:
        form = form_class(instance=instance)

        return render(request, template, {"form": form, "view_config": user})


@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if hasattr(user, "paciente"):
        user.paciente.delete()
    elif hasattr(user, "medico"):
        user.medico.delete()
    elif hasattr(user, "administrador"):
        user.administrador.delete()
    return redirect("dashboard:administrador_listas")


@login_required
@admin_required
def register_pac(request):
    form = PacienteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:administrador_listas")
    return render(
        request, "dashboard/administradores/lista/regpac.html", {"form": form}
    )


@login_required
@admin_required
def register_med(request):
    form = MedicoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:administrador_listas")
    return render(
        request, "dashboard/administradores/lista/regmed.html", {"form": form}
    )


@login_required
@admin_required
def register_adm(request):
    form = AdministradorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:administrador_listas")
    return render(
        request, "dashboard/administradores/lista/regadm.html", {"form": form}
    )


@login_required
def dashboard_view(request):
    user = request.user
    if hasattr(user, "administrador"):
        return redirect("dashboard:administrador")
    elif hasattr(user, "medico"):
        return redirect("dashboard:medico")
    elif hasattr(user, "paciente"):
        return redirect("dashboard:paciente")
    return redirect("users:login")


@login_required
@admin_required
def administrador(request):
    eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
    eventos_agendados = eventos.filter(status="AGENDADO").count()
    eventos_confirmados = eventos.filter(status="CONFIRMADO").count()
    eventos_cancelados = eventos.filter(status="CANCELADO").count()
    eventos_concluidos = eventos.filter(status="CONCLUIDO").count()
    eventos_ausentes = eventos.filter(status="AUSENTE").count()
    eventos_proximos = eventos.filter(
        status__in=["AGENDADO", "CONFIRMADO"], data_inicio__gte=timezone.now()
    ).order_by("data_inicio")
    proximo_agendamento = eventos_proximos.first()
    proxima_data = proximo_agendamento.data_inicio if proximo_agendamento else None

    eventos_lista = eventos.filter(
        status__in=["AGENDADO", "CONFIRMADO", "CANCELADO"],
        data_inicio__gte=timezone.now(),
    ).order_by("data_inicio")

    eventos_lista_concluidos = eventos.filter(
        status__in=["CONCLUIDO"],
        data_fim__lt=timezone.now(),
    ).order_by("data_fim")

    context = {
        "eventos_agendados": eventos_agendados,
        "eventos_confirmados": eventos_confirmados,
        "eventos_cancelados": eventos_cancelados,
        "eventos_concluidos": eventos_concluidos,
        "eventos_ausentes": eventos_ausentes,
        "eventos_lista": eventos_lista,
        "eventos_lista_concluidos": eventos_lista_concluidos,
        "proxima_data": proxima_data,
        "proximo_agendamento": proximo_agendamento,
    }
    return render(request, "dashboard/administradores/dashboard.html", context)


@login_required
@admin_required
def administrador_agendamentos(request):
    eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
    eventos_andamento = eventos.filter(
        data_inicio__lte=timezone.now(), data_fim__gte=timezone.now()
    )
    eventos_completos = eventos.filter(data_fim__lt=timezone.now())
    eventos_proximos = eventos.filter(data_inicio__gte=timezone.now())
    ultimos_eventos = eventos.order_by("-id")[:10]

    event_list = []
    for e in eventos:
        event_dict = {
            "id": e.id,
            "avatar": e.paciente.avatar.url if e.paciente.avatar else "",
            "paciente": e.paciente.username,
            "genero": e.paciente.genero,
            "data_nascimento": (
                e.paciente.data_nascimento.strftime("%Y-%m-%d")
                if e.paciente.data_nascimento
                else ""
            ),
            "procedimentos": e.procedimentos,
            "convenio": e.convenio,
            "observacoes": e.observacoes,
            "status": e.get_status_display(),
            "start": timezone.localtime(e.data_inicio).isoformat(),
            "end": timezone.localtime(e.data_fim).isoformat(),
        }
        event_list.append(event_dict)

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
def edit_agendamento(request, pk):
    evento = get_object_or_404(CriarEvento, pk=pk)

    if request.method == "POST":
        form = AgendamentoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("dashboard:calendar")
    else:
        form = AgendamentoForm(instance=evento)

    context = {
        "form": form,
        "evento": evento,
    }
    return render(request, "dashboard/administradores/editagendamentos.html", context)


@login_required
@admin_required
def administrador_lista(request):
    context = {
        "pacientes": Paciente.objects.all(),
        "medicos": Medico.objects.all(),
        "administradores": Administrador.objects.all(),
    }
    return render(request, "dashboard/administradores/listas.html", context)


@login_required
@medico_required
def medico(request):
    return render(request, "dashboard/medicos/dashboard.html")


@login_required
@paciente_required
def paciente(request):
    return render(request, "dashboard/pacientes/dashboard.html")


@login_required
@paciente_required
def paciente_agenda(request):
    return render(request, "dashboard/pacientes/agendamento.html")


class CalendarView(LoginRequiredMixin, generic.View):
    login_url = "users:login"
    template_name = "dashboard/administradores/agendamentos.html"

    def get(self, request):
        eventos = CriarEvento.objects.filter(is_active=True, is_deleted=False)
        event_list = []
        for e in eventos:
            event_dict = {
                "id": e.id,
                "title": e.paciente.username,
                "avatar": e.paciente.avatar.url if e.paciente.avatar else "",
                "paciente": e.paciente.username,
                "genero": e.paciente.genero,
                "data_nascimento": (
                    e.paciente.data_nascimento.strftime("%Y-%m-%d")
                    if e.paciente.data_nascimento
                    else ""
                ),
                "procedimentos": e.procedimentos,
                "convenio": e.convenio,
                "observacoes": e.observacoes,
                "status": e.get_status_display(),
                "start": timezone.localtime(e.data_inicio).isoformat(),
                "end": timezone.localtime(e.data_fim).isoformat(),
            }
            event_list.append(event_dict)

        return render(
            request,
            self.template_name,
            {
                "form": AgendamentoForm(),
                "eventos": json.dumps(event_list, default=str),
                "ultimos_eventos": eventos.order_by("-id")[:10],
            },
        )


@login_required
def create_agendamento(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            evento = form.save()
    return redirect("dashboard:calendar")


@login_required
def delete_agendamento(request, event_id):
    eventos = get_object_or_404(CriarEvento, id=event_id)
    if request.method == "POST":
        eventos.delete()
        return JsonResponse({"message": "Agendamento deletado com sucesso."})
    return JsonResponse({"message": "Erro!"}, status=400)

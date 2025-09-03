from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.utils import timezone
from users.models import Usuario, Paciente, Medico, Administrador
from users.decorators import admin_required, medico_required, paciente_required
from dashboard.forms import (
    PacienteForm,
    MedicoForm,
    AdministradorForm,
    AgendamentoForm,
    MarcarAgendamentoForm,
    BloquearDiaForm,
)
from dashboard.models import CriarEvento, MarcarEvento, BloquearDia
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
        return redirect("dashboard:prontuarios_adm")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
        return redirect("dashboard:prontuarios_adm")
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
            return redirect("dashboard:administradores")
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
    return redirect("dashboard:prontuarios_adm")


@login_required
@admin_required
def register_pac(request):
    form = PacienteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:prontuarios_adm")
    return render(
        request, "dashboard/administradores/lista/regpac.html", {"form": form}
    )


@login_required
@admin_required
def register_med(request):
    form = MedicoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:prontuarios_adm")
    return render(
        request, "dashboard/administradores/lista/regmed.html", {"form": form}
    )


@login_required
@admin_required
def register_adm(request):
    form = AdministradorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("dashboard:prontuarios_adm")
    return render(
        request, "dashboard/administradores/lista/regadm.html", {"form": form}
    )


def eventos_filtrados(user):
    base_query = CriarEvento.objects.filter(is_active=True, is_deleted=False)

    if hasattr(user, "paciente"):
        return base_query.filter(paciente=user.paciente)
    elif hasattr(user, "medico"):
        return base_query.filter(medico=user.medico)
    elif hasattr(user, "administrador"):
        return base_query

    return CriarEvento.objects.none()


@login_required
def dashboard_view(request):
    user = request.user
    if hasattr(user, "administrador"):
        return redirect("dashboard:administradores")
    elif hasattr(user, "medico"):
        return redirect("dashboard:medicos")
    elif hasattr(user, "paciente"):
        return redirect("dashboard:pacientes")
    return redirect("users:login")


@login_required
@admin_required
def administrador(request):
    eventos = eventos_filtrados(request.user)
    eventos_agendados = eventos.filter(status="AGENDADO").count()
    eventos_pedidos = eventos.filter(status="PEDIDOS").count()
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
        status__in=["AGENDADO", "PEDIDOS", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    ).order_by("data_inicio")

    eventos_lista_concluidos = eventos.filter(
        status__in=["CONCLUIDO"],
    ).order_by("data_fim")

    horario_atual = timezone.now().strftime("%H:%M:%S")
    data_atual = timezone.now().strftime("%Y/%m/%d")

    context = {
        "eventos_agendados": eventos_agendados,
        "eventos_pedidos": eventos_pedidos,
        "eventos_confirmados": eventos_confirmados,
        "eventos_cancelados": eventos_cancelados,
        "eventos_concluidos": eventos_concluidos,
        "eventos_ausentes": eventos_ausentes,
        "eventos_lista": eventos_lista,
        "eventos_lista_concluidos": eventos_lista_concluidos,
        "proxima_data": proxima_data,
        "proximo_agendamento": proximo_agendamento,
        "horario_atual": horario_atual,
        "data_atual": data_atual,
    }
    return render(request, "dashboard/administradores/dashboard.html", context)


@login_required
@admin_required
def administrador_agendamentos(request):
    eventos = eventos_filtrados(request.user)
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
            "title": f"{e.paciente.username}",
            "avatar": e.paciente.avatar.url if e.paciente.avatar else "",
            "paciente": e.paciente.username,
            "genero": e.paciente.genero,
            "data_nascimento": (e.paciente.data_nascimento.strftime("%Y-%m-%d") if e.paciente.data_nascimento else ""),
            "procedimentos": e.procedimentos,
            "convenio": e.convenio,
            "observacoes": e.observacoes,
            "status": e.get_status_display(),
            "start": timezone.localtime(e.data_inicio).isoformat(),
            "end": timezone.localtime(e.data_fim).isoformat(),
            "overlap": False,
        }
        event_list.append(event_dict)
    
    dias_bloqueados = BloquearDia.objects.filter(usuario=request.user)
    for dia in dias_bloqueados:
        bloqueio_dict = {
            "id": f"bloqueio-{dia.id}",
            "title": f"Dia Bloqueado - {dia.get_dia_escolhido_display()}",
            "daysOfWeek": [dia.dia_escolhido],
            "display": "background",
            "rendering": "background",
            "backgroundColor": "#D1D5DB",
            "allDay": True,
            "overlap": False,
        }
        event_list.append(bloqueio_dict)

    context = {
        "form": AgendamentoForm(),
        "form_2": BloquearDiaForm(),
        "ultimos_eventos": ultimos_eventos,
        "eventos_andamento": eventos_andamento,
        "eventos_completos": eventos_completos,
        "eventos_proximos": eventos_proximos,
        "eventos": json.dumps(event_list, default=str),
    }
    return render(request, "dashboard/administradores/agendamentos.html", context)


@login_required
@admin_required
def administrador_prontuario(request):
    context = {
        "pacientes": Paciente.objects.all(),
        "medicos": Medico.objects.all(),
        "administradores": Administrador.objects.all(),
    }
    return render(request, "dashboard/administradores/listas.html", context)


@login_required
@medico_required
def medico(request):
    eventos = eventos_filtrados(request.user)
    eventos_agendados = eventos.filter(status="AGENDADO").count()
    eventos_pedidos = eventos.filter(status="PEDIDOS").count()
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
        status__in=["AGENDADO", "PEDIDOS", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    ).order_by("data_inicio")

    eventos_lista_concluidos = eventos.filter(
        status__in=["CONCLUIDO"],
    ).order_by("data_fim")

    horario_atual = timezone.now().strftime("%H:%M:%S")
    data_atual = timezone.now().strftime("%Y/%m/%d")

    context = {
        "eventos_agendados": eventos_agendados,
        "eventos_pedidos": eventos_pedidos,
        "eventos_confirmados": eventos_confirmados,
        "eventos_cancelados": eventos_cancelados,
        "eventos_concluidos": eventos_concluidos,
        "eventos_ausentes": eventos_ausentes,
        "eventos_lista": eventos_lista,
        "eventos_lista_concluidos": eventos_lista_concluidos,
        "proxima_data": proxima_data,
        "proximo_agendamento": proximo_agendamento,
        "horario_atual": horario_atual,
        "data_atual": data_atual,
    }
    return render(request, "dashboard/medicos/dashboard.html", context)


@login_required
@medico_required
def medico_agendamentos(request):
    eventos = eventos_filtrados(request.user)
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
            "title": f"{e.paciente.username}",
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
        "form_2": BloquearDiaForm(),
        "ultimos_eventos": ultimos_eventos,
        "eventos_andamento": eventos_andamento,
        "eventos_completos": eventos_completos.count(),
        "eventos_proximos": eventos_proximos.count(),
        "eventos": json.dumps(event_list, default=str),
    }
    return render(request, "dashboard/medicos/agendamentos.html", context)


@login_required
@medico_required
def medico_prontuario(request):
    context = {
        "pacientes": Paciente.objects.all(),
        "medicos": Medico.objects.all(),
        "administradores": Administrador.objects.all(),
    }
    return render(request, "dashboard/medicos/listas.html", context)


@login_required
@paciente_required
def paciente(request):
    eventos = eventos_filtrados(request.user)
    eventos_agendados = eventos.filter(status="AGENDADO").count()
    eventos_pedidos = eventos.filter(status="PEDIDOS").count()
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
        status__in=["AGENDADO", "PEDIDOS", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    ).order_by("data_inicio")

    eventos_lista_pedidos = eventos.filter(
        status__in=["PEDIDOS"],
    ).order_by("data_fim")

    horario_atual = timezone.now().strftime("%H:%M:%S")
    data_atual = timezone.now().strftime("%Y/%m/%d")

    context = {
        "eventos_agendados": eventos_agendados,
        "eventos_pedidos": eventos_pedidos,
        "eventos_confirmados": eventos_confirmados,
        "eventos_cancelados": eventos_cancelados,
        "eventos_concluidos": eventos_concluidos,
        "eventos_ausentes": eventos_ausentes,
        "eventos_lista": eventos_lista,
        "eventos_lista_concluidos": eventos_lista_pedidos,
        "proxima_data": proxima_data,
        "proximo_agendamento": proximo_agendamento,
        "horario_atual": horario_atual,
        "data_atual": data_atual,
    }
    return render(request, "dashboard/pacientes/dashboard.html", context)


@login_required
@paciente_required
def paciente_agenda(request):
    eventos = eventos_filtrados(request.user)
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
    return render(request, "dashboard/pacientes/agendamentos.html", context)


def paciente_prontuario(request):
    return render(request, "dashboard/pacientes/prontuario.html")


@login_required
def create_agendamento(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)

            user = request.user
            if hasattr(user, "paciente"):
                evento.paciente = user.paciente
            elif hasattr(user, "medico"):
                evento.medico = user.medico

            evento.save()

            if hasattr(user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(user, "medico"):
                return redirect("dashboard:agenda_med")
            elif hasattr(user, "paciente"):
                return redirect("dashboard:agenda_pac")


@login_required
def create_consulta(request):
    if request.method == "POST":
        form = MarcarAgendamentoForm(request.POST)

        if form.is_valid():
            evento = form.save(commit=False)
            evento.save()

            return redirect("dashboard:pacientes")
    else:
        form = MarcarAgendamentoForm()

    return render(request, "dashboard/pacientes/createconsultas.html", {"form": form})


@login_required
def edit_agendamento(request, pk):
    user = request.user

    if hasattr(user, "paciente"):
        evento = get_object_or_404(CriarEvento, pk=pk, paciente=user.paciente)
    elif hasattr(user, "medico"):
        evento = get_object_or_404(CriarEvento, pk=pk, medico=user.medico)
    elif hasattr(user, "administrador"):
        evento = get_object_or_404(CriarEvento, pk=pk)

    def get_template():
        user = request.user
        if hasattr(user, "administrador"):
            return "dashboard/administradores/editagendamentos.html"
        elif hasattr(user, "medico"):
            return "dashboard/medicos/editagendamentos.html"

    if request.method == "POST":
        form = AgendamentoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            if hasattr(request.user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(request.user, "medico"):
                return redirect("dashboard:agenda_med")
    else:
        form = AgendamentoForm(instance=evento)

    context = {
        "form": form,
        "evento": evento,
    }
    return render(request, get_template(), context)


@login_required
def delete_agendamento(request, event_id):
    user = request.user

    if hasattr(user, "paciente"):
        eventos = get_object_or_404(CriarEvento, id=event_id, paciente=user.paciente)
    elif hasattr(user, "medico"):
        eventos = get_object_or_404(CriarEvento, id=event_id, medico=user.medico)
    elif hasattr(user, "administrador"):
        eventos = get_object_or_404(CriarEvento, id=event_id)
    else:
        return JsonResponse({"message": "Não autorizado!"}, status=403)

    if request.method == "POST":
        eventos.delete()
        return JsonResponse({"message": "Agendamento deletado com sucesso."})
    return JsonResponse({"message": "Erro!"}, status=400)

@login_required
def create_bloqueio(request):
    if request.method == "POST":
        form = BloquearDiaForm(request.POST)
        if form.is_valid():
            bloqueio = form.save(commit=False)
            bloqueio.usuario = request.user
            bloqueio.save()
            
            if hasattr(request.user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(request.user, "medico"):
                return redirect("dashboard:agenda_med")
        else:
            if hasattr(request.user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(request.user, "medico"):
                return redirect("dashboard:agenda_med")

    return redirect("users:login")
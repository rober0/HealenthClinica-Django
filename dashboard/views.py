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
    ListaEsperaForm,
    BloquearDiaForm,
)
from dashboard.models import CriarAgendamento, ListaEspera, BloquearDia
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
    base_query = CriarAgendamento.objects.filter(is_active=True, is_deleted=False)

    if hasattr(user, "paciente"):
        return base_query.filter(paciente=user.paciente)
    elif hasattr(user, "medico"):
        return base_query.filter(medico=user.medico)
    elif hasattr(user, "administrador"):
        return base_query

    return CriarAgendamento.objects.none()


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
    eventos_futuros = eventos.filter(
        status__in=["AGENDADO", "PEDIDO", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    )

    eventos_agendados = eventos_futuros.filter(status="AGENDADO").count()
    eventos_pedidos = eventos_futuros.filter(status="PEDIDOS").count()
    eventos_confirmados = eventos_futuros.filter(status="CONFIRMADO").count()
    eventos_cancelados = eventos_futuros.filter(status="CANCELADO").count()
    eventos_ausentes = eventos_futuros.filter(status="AUSENTE").count()
    eventos_concluidos = eventos.filter(status="CONCLUIDO").count()
    eventos_lista_concluidos = eventos.filter(status="CONCLUIDO").order_by("-data_fim")
    eventos_lista = eventos_futuros.order_by("data_inicio")
    proximo_agendamento = eventos_lista.first()
    proxima_data = proximo_agendamento.data_inicio if proximo_agendamento else None

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
    user = request.user

    eventos_do_admin = eventos_filtrados(user)
    eventos_disponiveis = eventos_do_admin.filter(
        status__in=["AGENDADO", "PEDIDO", "CONFIRMADO"],
    ).order_by("data_inicio")
    eventos_indisponiveis = ListaEspera.objects.all().order_by("created_at")

    event_list = []
    for e in eventos_do_admin:
        colors = {
            "Agendado": {"backgroundColor": "#2c5ee9ff", "borderColor": "#2c5ee9ff"},
            "Pedido": {"backgroundColor": "#eeae00ff", "borderColor": "#eeae00ff"},
            "Confirmado": {"backgroundColor": "#34D399", "borderColor": "#34D399"},
            "Cancelado": {"backgroundColor": "#EB2F2F", "borderColor": "#EB2F2F"},
            "Concluido": {"backgroundColor": "#3fa17dff", "borderColor": "#3fa17dff"},
            "Ausente": {"backgroundColor": "#b8b6b4ff", "borderColor": "#b8b6b4ff"},
        }
        status_display = e.get_status_display()
        event_dict = {
            "id": e.id,
            "title": f"{e.paciente.username} - {e.medico}",
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
            "status": status_display,
            "start": timezone.localtime(e.data_inicio).isoformat(),
            "end": timezone.localtime(e.data_fim).isoformat(),
            "overlap": False,
            **colors.get(status_display, {}),
            "textColor": "#FFFFFF",
        }
        event_list.append(event_dict)

    context = {
        "form": AgendamentoForm(),
        "form_2": BloquearDiaForm(),
        "eventos_disponiveis": eventos_disponiveis,
        "eventos_indisponiveis": eventos_indisponiveis,
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
    eventos_futuros = eventos.filter(
        status__in=["AGENDADO", "PEDIDO", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    )

    eventos_agendados = eventos_futuros.filter(status="AGENDADO").count()
    eventos_pedidos = eventos_futuros.filter(status="PEDIDOS").count()
    eventos_confirmados = eventos_futuros.filter(status="CONFIRMADO").count()
    eventos_cancelados = eventos_futuros.filter(status="CANCELADO").count()
    eventos_ausentes = eventos_futuros.filter(status="AUSENTE").count()
    eventos_concluidos = eventos.filter(status="CONCLUIDO").count()
    eventos_lista_concluidos = eventos.filter(status="CONCLUIDO").order_by("-data_fim")
    eventos_lista = eventos_futuros.order_by("data_inicio")
    proximo_agendamento = eventos_lista.first()
    proxima_data = proximo_agendamento.data_inicio if proximo_agendamento else None
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
    user = request.user

    eventos_do_medico = eventos_filtrados(user)
    eventos_disponiveis = eventos_do_medico.filter(
        status__in=["AGENDADO", "PEDIDO", "CONFIRMADO"],
    ).order_by("data_inicio")
    eventos_indisponiveis = ListaEspera.objects.filter(medico=user.medico).order_by(
        "created_at"
    )

    event_list = []
    for e in eventos_do_medico:
        colors = {
            "Agendado": {"backgroundColor": "#2c5ee9ff", "borderColor": "#2c5ee9ff"},
            "Pedido": {"backgroundColor": "#eeae00ff", "borderColor": "#eeae00ff"},
            "Confirmado": {"backgroundColor": "#34D399", "borderColor": "#34D399"},
            "Cancelado": {"backgroundColor": "#EB2F2F", "borderColor": "#EB2F2F"},
            "Concluido": {"backgroundColor": "#3fa17dff", "borderColor": "#3fa17dff"},
            "Ausente": {"backgroundColor": "#b8b6b4ff", "borderColor": "#b8b6b4ff"},
        }
        status_display = e.get_status_display()
        event_dict = {
            "id": e.id,
            "title": f"{e.paciente.username} - {e.medico}",
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
            "status": status_display,
            "start": timezone.localtime(e.data_inicio).isoformat(),
            "end": timezone.localtime(e.data_fim).isoformat(),
            "overlap": False,
            **colors.get(status_display, {}),
            "textColor": "#FFFFFF",
        }
        event_list.append(event_dict)

    dias_bloqueados = BloquearDia.objects.filter(medico=user)
    for dia in dias_bloqueados:
        bloqueio_dict = {
            "id": f"bloqueio-{dia.id}",
            "title": f"Horário Bloqueado",
            "daysOfWeek": [dia.dia_escolhido],
            "display": "background",
            "backgroundColor": "#D1D5DB",
            "allDay": False,
            "overlap": False,
            "startTime": dia.horario_inicio.strftime("%H:%M:%S"),
            "endTime": dia.horario_fim.strftime("%H:%M:%S"),
        }
        event_list.append(bloqueio_dict)

    context = {
        "form": AgendamentoForm(),
        "form_2": BloquearDiaForm(),
        "eventos_disponiveis": eventos_disponiveis,
        "eventos_indisponiveis": eventos_indisponiveis,
        "eventos": json.dumps(event_list, default=str),
    }

    return render(request, "dashboard/medicos/agendamentos.html", context)


@login_required
@medico_required
def medico_prontuario(request):
    context = {
        "pacientes": Paciente.objects.all(),
    }
    return render(request, "dashboard/medicos/listas.html", context)


@login_required
@paciente_required
def paciente(request):
    eventos = eventos_filtrados(request.user)
    eventos_futuros = eventos.filter(
        status__in=["AGENDADO", "PEDIDO", "CONFIRMADO", "CANCELADO", "AUSENTE"],
        data_inicio__gte=timezone.now(),
    )

    eventos_agendados = eventos_futuros.filter(status="AGENDADO").count()
    eventos_pedidos = eventos_futuros.filter(status="PEDIDOS").count()
    eventos_confirmados = eventos_futuros.filter(status="CONFIRMADO").count()
    eventos_cancelados = eventos_futuros.filter(status="CANCELADO").count()
    eventos_ausentes = eventos_futuros.filter(status="AUSENTE").count()
    eventos_concluidos = eventos.filter(status="CONCLUIDO").count()
    eventos_lista = eventos_futuros.order_by("data_inicio")
    eventos_consulta = eventos_futuros.order_by("data_inicio").filter(status="PEDIDO")
    proximo_agendamento = eventos_lista.first()
    proxima_data = proximo_agendamento.data_inicio if proximo_agendamento else None
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
        "eventos_consulta": eventos_consulta,
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
        colors = {
            "Agendado": {"backgroundColor": "#2c5ee9ff", "borderColor": "#2c5ee9ff"},
            "Pedido": {"backgroundColor": "#eeae00ff", "borderColor": "#eeae00ff"},
            "Confirmado": {"backgroundColor": "#34D399", "borderColor": "#34D399"},
            "Cancelado": {"backgroundColor": "#EB2F2F", "borderColor": "#EB2F2F"},
            "Concluido": {"backgroundColor": "#3fa17dff", "borderColor": "#3fa17dff"},
            "Ausente": {"backgroundColor": "#b8b6b4ff", "borderColor": "#b8b6b4ff"},
        }
        status_display = e.get_status_display()
        event_dict = {
            "id": e.id,
            "title": f"{e.paciente.username} - {e.medico}",
            "avatar": e.paciente.avatar.url if e.paciente.avatar else "",
            "paciente": e.paciente.username,
            "medico": f"Dr.(A) {e.medico.username}",
            "genero": e.paciente.genero,
            "data_nascimento": (
                e.paciente.data_nascimento.strftime("%Y-%m-%d")
                if e.paciente.data_nascimento
                else ""
            ),
            "procedimentos": e.procedimentos,
            "convenio": e.convenio,
            "observacoes": e.observacoes,
            "status": status_display,
            "start": timezone.localtime(e.data_inicio).isoformat(),
            "end": timezone.localtime(e.data_fim).isoformat(),
            "overlap": False,
            **colors.get(status_display, {}),
            "textColor": "#FFFFFF",
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
    context = {"medicos": Medico.objects.all()}
    return render(request, "dashboard/pacientes/listas.html", context)


@login_required
def create_agendamento(request):
    user = request.user
    if request.method == "POST":
        post_data = request.POST.copy()

        post_data["status"] = "AGENDADO"
    if hasattr(user, "medico"):
        post_data["medico"] = user.medico.pk

    form = AgendamentoForm(post_data)

    if form.is_valid():
        form.save()

        if hasattr(user, "administrador"):
            return redirect("dashboard:agenda_adm")
        elif hasattr(user, "medico"):
            return redirect("dashboard:agenda_med")

    else:
        if hasattr(form, "_is_conflict") and form._is_conflict:
            ListaEspera.objects.create(
                paciente_id=form.data.get("paciente"),
                medico_id=form.data.get("medico"),
                procedimentos=form.data.get("procedimentos"),
                convenio=form.data.get("convenio"),
                observacoes=form.data.get("observacoes"),
                data_inicio=form.data.get("data_inicio"),
                data_fim=form.data.get("data_fim"),
            )
            if hasattr(user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(user, "medico"):
                return redirect("dashboard:agenda_med")

        print("Erro")
        print(form.errors.as_json())

        if hasattr(user, "administrador"):
            return redirect("dashboard:agenda_adm")
        elif hasattr(user, "medico"):
            return redirect("dashboard:agenda_med")


@login_required
@paciente_required
def create_consulta(request):
    if request.method == "POST":
        form = MarcarAgendamentoForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data["data_inicio"]
            data_fim = form.cleaned_data["data_fim"]
            medico_selecionado = form.cleaned_data["medico"]
            paciente_atual = request.user.paciente

            agendamentos_conflitantes = CriarAgendamento.objects.filter(
                medico=medico_selecionado,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio,
                is_deleted=False,
            ).exists()

            if agendamentos_conflitantes:
                ListaEspera.objects.create(
                    paciente=paciente_atual,
                    medico=medico_selecionado,
                    procedimentos="Consulta",
                    convenio=form.cleaned_data["convenio"],
                    queixa=form.cleaned_data["queixa"],
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                )
            else:
                evento = form.save(commit=False)
                evento.paciente = paciente_atual
                evento.status = "PEDIDO"
                evento.procedimentos = "Consulta"
                evento.save()

            return redirect("dashboard:pacientes")
    else:
        form = MarcarAgendamentoForm()

    return render(request, "dashboard/pacientes/createconsultas.html", {"form": form})


@login_required
def edit_agendamento(request, pk):
    user = request.user

    if hasattr(user, "paciente"):
        evento = get_object_or_404(CriarAgendamento, pk=pk, paciente=user.paciente)
    elif hasattr(user, "medico"):
        evento = get_object_or_404(CriarAgendamento, pk=pk, medico=user.medico)
    elif hasattr(user, "administrador"):
        evento = get_object_or_404(CriarAgendamento, pk=pk)

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
def delete_agendamento(request, agendamento_id):
    user = request.user

    if hasattr(user, "paciente"):
        eventos = get_object_or_404(CriarAgendamento, id=agendamento_id, paciente=user.paciente)
    elif hasattr(user, "medico"):
        eventos = get_object_or_404(CriarAgendamento, id=agendamento_id, medico=user.medico)
    elif hasattr(user, "administrador"):
        eventos = get_object_or_404(CriarAgendamento, id=agendamento_id)
    else:
        return JsonResponse({"message": "Não autorizado!"}, status=403)

    if request.method == "POST":
        eventos.delete()
        return JsonResponse({"message": "Agendamento deletado com sucesso."})
    return JsonResponse({"message": "Erro!"}, status=400)

@login_required
def edit_lista_espera(request, pk):
    user = request.user

    if hasattr(user, "medico"):
        espera = get_object_or_404(ListaEspera, pk=pk, medico=user.medico)
    elif hasattr(user, "administrador"):
        espera = get_object_or_404(ListaEspera, pk=pk)

    def get_template():
        user = request.user
        if hasattr(user, "administrador"):
            return "dashboard/administradores/editlistaespera.html"
        elif hasattr(user, "medico"):
            return "dashboard/medicos/editlistaespera.html"

    if request.method == "POST":
        form = ListaEsperaForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data["data_inicio"]
            data_fim = form.cleaned_data["data_fim"]
            medico_selecionado = espera.medico
            paciente_atual = espera.paciente

            agendamentos_conflitantes = CriarAgendamento.objects.filter(
                medico=medico_selecionado,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio,
                is_deleted=False,
            ).exists()

            if not agendamentos_conflitantes:
                evento = form.save(commit=False)
                evento.paciente = paciente_atual
                evento.medico = medico_selecionado
                evento.status = "AGENDADO"
                evento.procedimentos = espera.procedimentos
                evento.convenio = espera.convenio
                evento.observacoes = espera.observacoes
                evento.queixa = espera.queixa
                evento.save()
                espera.delete()

                if hasattr(request.user, "administrador"):
                    return redirect("dashboard:agenda_adm")
                elif hasattr(request.user, "medico"):
                    return redirect("dashboard:agenda_med")
            else:
                form.add_error(None, "Conflito de agendamento. Tente outro horário.")
    else:
        initial_data = {
            "paciente": espera.paciente,
            "medico": espera.medico,
            "procedimentos": espera.procedimentos,
            "convenio": espera.convenio,
            "observacoes": espera.observacoes,
            "queixa": espera.queixa,
            "data_inicio": espera.data_inicio,
            "data_fim": espera.data_fim,
        }
        form = ListaEsperaForm(initial=initial_data)

    context = {
        "form": form,
        "espera": espera,
    }
    return render(request, get_template(), context)

@login_required
def delete_lista_espera(request, lista_espera_id):
    user = request.user

    if hasattr(user, "medico"):
        espera = get_object_or_404(ListaEspera, id=lista_espera_id, medico=user.medico)
    elif hasattr(user, "administrador"):
        espera = get_object_or_404(ListaEspera, id=lista_espera_id)
    else:
        return JsonResponse({"message": "Não autorizado!"}, status=403)

    if request.method == "POST":
        espera.delete()
        if hasattr(user, "medico"):
            return redirect("dashboard:agenda_med")
        elif hasattr(user, "administrador"):
            return redirect("dashboard:agenda_adm")
    return JsonResponse({"message": "Erro!"}, status=400)

@login_required
def create_bloqueio(request):
    user = request.user
    if request.method == "POST":
        post_data = request.POST.copy()
        if hasattr(user, "medico"):
            post_data["medico"] = user.medico.pk
        form = BloquearDiaForm(post_data)
        if form.is_valid():
            form.save()   
            
            if hasattr(request.user, "administrador"):
                return redirect("dashboard:agenda_adm")
            elif hasattr(request.user, "medico"):
                return redirect("dashboard:agenda_med")
        else:
            if hasattr(request.user, "administrador"):
                context = {"form_2": form}
                return render(
                    request, "dashboard/administradores/agendamentos.html", context
                )
            elif hasattr(request.user, "medico"):
                context = {"form_2": form}
                return render(request, "dashboard/medicos/agendamentos.html", context)

    return redirect("users:login")

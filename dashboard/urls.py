from django.urls import path
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "dashboard"

urlpatterns = [
    path("pacientes/", views.paciente, name="pacientes"),
    path("pacientes/agendamentos", views.paciente_agenda, name="agenda_pac"),
    path(
        "pacientes/agendamentos/novo", views.create_consulta, name="create_agenda_pac"
    ),
    path("pacientes/prontuario", views.paciente_prontuario, name="prontuarios_pac"),
    path("pacientes/settings", views.view_config, name="view_config_pac"),
    path("medicos/", views.medico, name="medicos"),
    path("medicos/agendamentos", views.medico_agendamentos, name="agenda_med"),
    path(
        "medicos/agendamentos/novo", views.create_agendamento, name="create_agenda_med"
    ),
    path(
        "medicos/agendamentos/editar/<int:pk>",
        views.edit_agendamento,
        name="edit_agenda_med",
    ),
    path(
        "medicos/agendamentos/deletar/<int:event_id>",
        views.delete_agendamento,
        name="delete_agenda_med",
    ),
    path(
        "medicos/bloquear-dia/",
        views.create_bloqueio,
        name="create_bloqueio_med",
    ),
    path("medicos/prontuario", views.medico_prontuario, name="prontuarios_med"),
    path("medicos/settings", views.view_config, name="view_config_med"),
    path("administradores/", views.administrador, name="administradores"),
    path(
        "administradores/agendamentos",
        views.administrador_agendamentos,
        name="agenda_adm",
    ),
    path(
        "administradores/agendamentos/novo",
        views.create_agendamento,
        name="create_agenda_adm",
    ),
    path(
        "administradores/agendamentos/editar/<int:pk>",
        views.edit_agendamento,
        name="edit_agenda_adm",
    ),
    path(
        "administradores/agendamentos/deletar/<int:event_id>",
        views.delete_agendamento,
        name="delete_agenda_adm",
    ),
    path(
        "administradores/bloquear-dia/",
        views.create_bloqueio,
        name="create_bloqueio_adm",
    ),
    path(
        "administradores/prontuario",
        views.administrador_prontuario,
        name="prontuarios_adm",
    ),
    path("administradores/settings", views.view_config, name="view_config_adm"),
    path("administradores/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path(
        "administradores/delete/<int:user_id>/", views.delete_user, name="delete_user"
    ),
    path(
        "administradores/registrar-paciente/", views.register_pac, name="register_pac"
    ),
    path("administradores/registrar-medico/", views.register_med, name="register_med"),
    path(
        "administradores/registrar-administrador/",
        views.register_adm,
        name="register_adm",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

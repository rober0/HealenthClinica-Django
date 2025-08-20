from django.urls import path
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "dashboard"

urlpatterns = [
    path("pacientes/", views.paciente, name="pacientes"),
    path("pacientes/agendamentos", views.paciente_agenda, name="agendapacientes"),
    path("pacientes/settings", views.view_config, name="view_config"),
    path("medicos/", views.medico, name="medicos"),
    path("medicos/agendamentos", views.CalendarView.as_view(), name="agenda_adm"),
    path(
        "medicos/agendamentos/novo", views.create_agendamento, name="create_event"
    ),
    path(
        "medicos/agendamentos/editar/<int:pk>",
        views.edit_agendamento,
        name="edit_event",
    ),
    path(
        "medicos/agendamentos/deletar/<int:event_id>",
        views.delete_agendamento,
        name="delete_event",
    ),
    path("medicos/prontuario", views.medicos_prontuario, name="medicos_prontuario"),
    path("medicos/settings", views.view_config, name="view_config"),
    path("administrador/", views.administrador, name="administrador"),
    path("administrador/agendamentos", views.CalendarView.as_view(), name="agenda_adm"),
    path(
        "administrador/agendamentos/novo", views.create_agendamento, name="create_event"
    ),
    path(
        "administrador/agendamentos/editar/<int:pk>",
        views.edit_agendamento,
        name="edit_event",
    ),
    path(
        "administrador/agendamentos/deletar/<int:event_id>",
        views.delete_agendamento,
        name="delete_event",
    ),
    path("administrador/prontuario", views.administrador_prontuario, name="administrador_listas"),
    path("administrador/settings", views.view_config, name="view_config"),
    path("administrador/edit/<int:user_id>/", views.edit_user, name="edit"),
    path("administrador/delete/<int:user_id>/", views.delete_user, name="delete"),
    path("administrador/registrar-paciente/", views.register_pac, name="regpac"),
    path("administrador/registrar-medico/", views.register_med, name="regmed"),
    path("administrador/registrar-administrador/", views.register_adm, name="regadm"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    path('pacientes/', views.paciente, name='pacientes'),
    path('pacientes/agendamentos', views.paciente_agenda, name='agendapacientes'),
    path('pacientes/settings', views.view_config, name='view_config'),
    # path('pacientes/medicos', views.pacientes_agendamedico, name='agendapacientesmed'),
    path('medicos/', views.medico, name='medicos'),
    # path('medicos/agendamentos', views.medicos_agenda, name='agendamedicos'),
    path('administrador/', views.administrador, name='administrador'),
    path('administrador/agendamentos', views.administrador_agendamentos, name='administrador_agendamentos'),
    path('administrador/lista', views.administrador_lista, name='administrador_listas'),
    path('administrador/settings', views.view_config, name='view_config'),
    path('administrador/edit/<int:user_id>/', views.edit_user, name='edit'),
    path('administrador/delete/<int:user_id>/', views.delete_user, name='delete'),
    path('administrador/registrar-paciente/', views.register_pac, name='regpac'),
    path('administrador/registrar-medico/', views.register_med, name='regmed'),
    path('administrador/registrar-administrador/', views.register_adm, name='regadm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
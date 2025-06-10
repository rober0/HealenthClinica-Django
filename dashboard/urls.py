from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    path('pacientes/', views.paciente, name='pacientes'),
    path('pacientes/agendamentos', views.paciente_agenda, name='agendapacientes'),
    # path('pacientes/medicos', views.pacientes_agendamedico, name='agendapacientesmed'),
    path('medicos/', views.medico, name='medicos'),
    # path('medicos/agendamentos', views.medicos_agenda, name='agendamedicos'),
    path('administrador/', views.administrador, name='administrador'),
    path('administrador/agendamentos', views.administrador_agendamentos, name='administrador_agendamentos'),
    path('administrador/lista', views.administrador_lista, name='administrador_listas'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
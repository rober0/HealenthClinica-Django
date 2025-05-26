from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes/agendamentos', views.pacientes_agenda, name='agendapacientes'),
    path('pacientes/medicos', views.pacientes_agendamedico, name='agendapacientesmed'),
    path('medicos/', views.medicos, name='medicos'),
    path('medicos/agendamentos', views.medicos_agenda, name='agendamedicos'),
    path('administrador/', views.administrador, name='administrador'),
    path('administrador/medicos', views.administrador_medicos, name='administrador_medicos'),
    path('administrador/pacientes', views.administrador_pacientes, name='administrador_pacientes'),
    path('administrador/medicos/agendamentos', views.administrador_medicos_agendamentos, name='administrador_medicos_agendamentos'),
    path('administrador/pacientes/agendamentos', views.administrador_pacientes_agendamentos, name='administrador_pacientes_agendamentos'),    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
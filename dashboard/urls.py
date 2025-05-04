from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('medicos/', views.medicos, name='medicos'),
]

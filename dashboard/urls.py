from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('medicos/', views.medicos, name='medicos'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
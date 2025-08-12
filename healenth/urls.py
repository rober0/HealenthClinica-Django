"""
URL configuration for healenth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "healenth"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("users/", include("users.urls", namespace="users")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("procedimentos/", views.procedimentos, name="procedimentos"),
    path("faq/", views.faq, name="faq"),
    path("quemsomos/", views.quemsomos, name="quemsomos"),
    path("termos/", views.termos, name="termos"),
    path("agendamedica/", views.agendamedica, name="agendamedica"),
    path("gestao/", views.gestao, name="gestao"),
    path("prontuario/", views.prontuario, name="prontuario"),
    path("faleconosco/", include("contato.urls")),
    path("sugestoes/", views.sugestoes, name="sugestoes"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

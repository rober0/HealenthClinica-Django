from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("fale-conosco", views.contato_view, name="fale-conosco"),
    path("sugestoes", views.sugestao_view, name="sugestoes"),
]

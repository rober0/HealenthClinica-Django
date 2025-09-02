from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "contato"

urlpatterns = [
    path("fale-conosco/", views.contato_view, name="contact-us"),
    path("sugestoes/", views.sugestao_view, name="review-us"),
]

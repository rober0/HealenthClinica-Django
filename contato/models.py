from django.db import models
from django.utils.translation import gettext_lazy as _


class Contato(models.Model):
    class categoriaChoices(models.TextChoices):
        SUP = "SUP", _("Suporte")
        CRI = "CRI", _("Crítica")
        OUT = "OUT", _("Outros")

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    categoria = models.CharField(
        max_length=3,
        choices=categoriaChoices.choices,
    )
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nomeC} - {self.get_categoria_display()}"


class Sugestao(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    sugestao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nomeS}"

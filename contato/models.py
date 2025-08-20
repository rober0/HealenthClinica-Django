from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _


class Contato(models.Model):
    class solicitanteChoices(models.TextChoices):
        PAC = 'PAC', _('PACIENTE')
        MED = 'MED', _('MÉDICO')
    class categoriaChoices(models.TextChoices):
        SUP = 'SUP', _('Suporte')
        CRI = 'CRI', _('Crítica')
        OUT = 'OUT', _('Outros')
    solicitanteC = models.CharField(max_length=3, choices=solicitanteChoices.choices, default=solicitanteChoices.PAC)
    nomeC = models.CharField(max_length=100)
    emailC = models.EmailField()
    categoria = models.CharField(max_length=3, choices=categoriaChoices.choices,)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nomeC} - {self.get_categoria_display()}"


class Sugestao(models.Model):
    class solicitanteSChoices(models.TextChoices):
        PAC = 'PAC', _('PACIENTE')
        MED = 'MED', _('MÉDICO')
    class procedimentosChoices(models.TextChoices):
        CO = 'CO', _('Consulta')
        EX = 'EX', _('Exame')
        RA = 'RA', _('Radiografia')
    class convenioChoices(models.TextChoices):
        PU = 'PU', _('Público')
        PR = 'PR', _('Privado')
        EM = 'EM', _('Empresarial')
    solicitanteS = models.CharField(max_length=3, choices=solicitanteSChoices.choices, default=solicitanteSChoices.PAC)
    nomeS = models.CharField(max_length=100)
    emailS = models.EmailField()
    procedimentosS = models.CharField(max_length=2, choices=procedimentosChoices.choices, default=procedimentosChoices.CO)
    convenio = models.CharField(max_length=2, choices=convenioChoices.choices, default=convenioChoices.PU)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nomeS}"
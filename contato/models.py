from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _


class Contato(models.Model):
    nomeC = models.CharField(max_length=100)
    emailC = models.EmailField()
    categoria = models.CharField(max_length=20)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nomeC

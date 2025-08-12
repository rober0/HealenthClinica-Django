from datetime import datetime
from django.db import models
from django.urls import reverse
from users.models import Paciente
from django.utils import timezone


class GerenciadorEvento(models.Manager):

    def eventos_andamento(self, paciente):
        today = datetime.now().date()
        return self.filter(
            paciente=paciente,
            is_active=True,
            is_deleted=False,
            data_inicio__lte=today,
            data_fim__gte=today,
        ).order_by("data_inicio")

    def eventos_completos(self, paciente):
        today = datetime.now().date()
        return self.filter(
            paciente=paciente, is_active=True, is_deleted=False, data_fim__lt=today
        )

    def eventos_proximos(self, paciente):
        today = timezone.now().date()
        return self.filter(
            paciente=paciente, is_active=True, is_deleted=False, data_inicio__gte=today
        ).order_by("data_inicio")

    def eventos_calendario(self, paciente):
        now = timezone.now()
        return self.filter(
            paciente=paciente, is_active=True, is_deleted=False, data_fim__gte=now
        ).order_by("data_inicio")


class AbstratoEvento(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CriarEvento(AbstratoEvento):
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('CONCLUIDO', 'Concluido'),
        ('AUSENTE', 'Ausente'),
    ]
    
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="paciente"
    )
    procedimentos = models.CharField(max_length=200)
    convenio = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='AGENDADO', null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    objects = GerenciadorEvento()
    
    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

class MembroEvento(AbstratoEvento):
    eventos = models.ForeignKey(
        CriarEvento, on_delete=models.CASCADE, related_name="eventos"
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="membro_evento"
    )

    class Meta:
        unique_together = ["eventos", "paciente"]

    def __str__(self):
        return str(self.paciente)

from datetime import datetime
from django.db import models
from users.models import Paciente, Medico
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
        ("AGENDADO", "Agendado"),
        ("CONFIRMADO", "Confirmado"),
        ("CANCELADO", "Cancelado"),
        ("CONCLUIDO", "Concluido"),
        ("AUSENTE", "Ausente"),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="paciente"
    )
    procedimentos = models.CharField(max_length=200)
    convenio = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="AGENDADO", null=True, blank=True
    )
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    objects = GerenciadorEvento()

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"


class CriarEventoPaciente(AbstratoEvento):
    STATUS_CHOICES = [
        ("PEDIDO", "Pedido"),
        ("AGENDADO", "Agendado"),
        ("CONFIRMADO", "Confirmado"),
        ("CANCELADO", "Cancelado"),
        ("CONCLUIDO", "Concluido"),
    ]

    paciente = models.ForeignKey(
        Paciente,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="paciente_evento",
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="medico_evento"
    )
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="PEDIDO", null=True, blank=True
    )
    queixa = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)

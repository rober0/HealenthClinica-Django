from datetime import datetime
from django.db import models
from users.models import Paciente, Medico
from django.utils import timezone
import datetime


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


class CriarAgendamento(models.Model):
    STATUS_CHOICES = [
        ("AGENDADO", "Agendado"),
        ("PEDIDO", "Pedido"),
        ("CONFIRMADO", "Confirmado"),
        ("CANCELADO", "Cancelado"),
        ("CONCLUIDO", "Concluido"),
        ("AUSENTE", "Ausente"),
    ]

    PROCEDIMENTOS_CHOICES = [
        ("", "Selecione um Procedimento"),
        ("Consulta", "Consulta"),
        ("Exame", "Exame"),
        ("Retorno", "Retorno"),
    ]

    CONVENIO_CHOICES = [
        ("", "Selecione um Convênio"),
        ("Publico", "Público"),
        ("Particular", "Particular"),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="agendamentos_paciente"
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="agendamentos_medico",
    )
    procedimentos = models.CharField(
        max_length=200, choices=PROCEDIMENTOS_CHOICES, default="Consulta"
    )
    convenio = models.CharField(max_length=100, choices=CONVENIO_CHOICES, default="")
    observacoes = models.TextField(blank=True, null=True)
    queixa = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="AGENDADO")
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GerenciadorEvento()

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"


class ListaEspera(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="lista_espera_paciente"
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="lista_espera_medico",
        blank=True,
        null=True,
    )
    procedimentos = models.CharField(
        max_length=200, choices=CriarAgendamento.PROCEDIMENTOS_CHOICES, default="Consulta"
    )
    convenio = models.CharField(
        max_length=100,
        choices=CriarAgendamento.CONVENIO_CHOICES,
        default="",
        null=True,
        blank=True,
    )
    observacoes = models.TextField(blank=True, null=True)
    queixa = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lista de Espera"
        verbose_name_plural = "Listas de Espera"


class BloquearDia(models.Model):
    DIAS_CHOICES = [
        (0, "Domingo"),
        (1, "Segunda-Feira"),
        (2, "Terça-Feira"),
        (3, "Quarta-Feira"),
        (4, "Quinta-Feira"),
        (5, "Sexta-Feira"),
        (6, "Sábado"),
    ]
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="dia_bloqueado_medico", null=True, blank=True
    )
    dia_escolhido = models.IntegerField(
        choices=DIAS_CHOICES, verbose_name="Dia da Semana"
    )
    horario_inicio = models.TimeField(
        verbose_name="Horário de Início do Bloqueio",
        default=datetime.time(0, 0),
        null=True,
        blank=True,
    )
    horario_fim = models.TimeField(
        verbose_name="Horário de Fim do Bloqueio",
        default=datetime.time(0, 0),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dia Bloqueado"
        verbose_name_plural = "Dias Bloqueados"
        unique_together = ("dia_escolhido", "medico")

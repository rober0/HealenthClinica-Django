from django.contrib import admin
from . import models


@admin.register(models.CriarEvento)
class AgendamentoAdmin(admin.ModelAdmin):
    model = models.CriarEvento
    list_display = [
        "id",
        "paciente",
        "medico",
        "procedimentos",
        "convenio",
        "observacoes",
        "data_inicio",
        "data_fim",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = [
        "paciente__username",
        "medico__username",
        "procedimentos",
        "convenio",
    ]

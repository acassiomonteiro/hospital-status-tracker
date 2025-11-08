from django.contrib import admin
from .models import Atendimento


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'profissional_responsavel', 'data_hora_entrada', 'status', 'atualizado_em']
    list_filter = ['status', 'data_hora_entrada', 'profissional_responsavel']
    search_fields = ['paciente__nome', 'paciente__cpf', 'queixa']
    readonly_fields = ['data_hora_entrada', 'atualizado_em']
    raw_id_fields = ['paciente', 'profissional_responsavel']

    fieldsets = (
        ('Paciente', {
            'fields': ('paciente',)
        }),
        ('Atendimento', {
            'fields': ('profissional_responsavel', 'queixa', 'status')
        }),
        ('Informações de Sistema', {
            'fields': ('data_hora_entrada', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

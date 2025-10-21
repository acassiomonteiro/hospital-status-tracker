from django.contrib import admin
from .models import Paciente, Atendimento


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'criado_em']
    search_fields = ['nome', 'cpf']
    list_filter = ['criado_em']
    readonly_fields = ['criado_em']


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'data_hora_entrada', 'status', 'atualizado_em']
    list_filter = ['status', 'data_hora_entrada']
    search_fields = ['paciente__nome', 'paciente__cpf', 'queixa']
    readonly_fields = ['data_hora_entrada', 'atualizado_em']
    raw_id_fields = ['paciente']

    fieldsets = (
        ('Paciente', {
            'fields': ('paciente',)
        }),
        ('Atendimento', {
            'fields': ('queixa', 'status')
        }),
        ('Informações de Sistema', {
            'fields': ('data_hora_entrada', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

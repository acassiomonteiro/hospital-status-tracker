from django.contrib import admin
from .models import Paciente, Atendimento, Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['user', 'perfil', 'registro_profissional', 'criado_em']
    list_filter = ['perfil', 'criado_em']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'registro_profissional']
    readonly_fields = ['criado_em']
    raw_id_fields = ['user']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'criado_em']
    search_fields = ['nome', 'cpf']
    list_filter = ['criado_em']
    readonly_fields = ['criado_em']


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

from django.contrib import admin
from .models import Evolucao


@admin.register(Evolucao)
class EvolucaoAdmin(admin.ModelAdmin):
    list_display = ['atendimento', 'tipo', 'profissional', 'data_hora']
    list_filter = ['tipo', 'data_hora', 'profissional']
    search_fields = ['atendimento__paciente__nome', 'descricao', 'profissional__user__username']
    readonly_fields = ['data_hora']
    raw_id_fields = ['atendimento', 'profissional']

    fieldsets = (
        ('Atendimento', {
            'fields': ('atendimento',)
        }),
        ('Evolução', {
            'fields': ('tipo', 'profissional', 'descricao')
        }),
        ('Informações de Sistema', {
            'fields': ('data_hora',),
            'classes': ('collapse',)
        }),
    )

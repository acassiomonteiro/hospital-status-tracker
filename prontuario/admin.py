from django.contrib import admin
from .models import Evolucao, SinalVital


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


@admin.register(SinalVital)
class SinalVitalAdmin(admin.ModelAdmin):
    list_display = [
        'atendimento',
        'data_hora',
        'get_pressao_arterial',
        'frequencia_cardiaca',
        'temperatura',
        'saturacao_o2',
        'profissional'
    ]
    list_filter = ['data_hora', 'profissional']
    search_fields = ['atendimento__paciente__nome', 'observacoes', 'profissional__user__username']
    readonly_fields = ['data_hora']
    raw_id_fields = ['atendimento', 'profissional']

    fieldsets = (
        ('Atendimento', {
            'fields': ('atendimento', 'profissional')
        }),
        ('Pressão Arterial', {
            'fields': ('pressao_arterial_sistolica', 'pressao_arterial_diastolica')
        }),
        ('Frequências', {
            'fields': ('frequencia_cardiaca', 'frequencia_respiratoria')
        }),
        ('Outros Sinais', {
            'fields': ('temperatura', 'saturacao_o2', 'glicemia')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Informações de Sistema', {
            'fields': ('data_hora',),
            'classes': ('collapse',)
        }),
    )

    def get_pressao_arterial(self, obj):
        """Exibe pressão arterial formatada no list_display"""
        return obj.get_pressao_arterial()
    get_pressao_arterial.short_description = 'Pressão Arterial'

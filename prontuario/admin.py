from django.contrib import admin
from .models import Evolucao, SinalVital, Prescricao, ItemPrescricao


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


class ItemPrescricaoInline(admin.TabularInline):
    """Inline para exibir/editar itens da prescrição"""
    model = ItemPrescricao
    extra = 1
    fields = ['medicamento', 'dose', 'via', 'frequencia', 'duracao_dias', 'observacoes_item']


@admin.register(Prescricao)
class PrescricaoAdmin(admin.ModelAdmin):
    list_display = ['atendimento', 'profissional', 'data_prescricao', 'validade', 'status', 'total_itens']
    list_filter = ['status', 'data_prescricao', 'profissional']
    search_fields = ['atendimento__paciente__nome', 'observacoes', 'profissional__user__username']
    readonly_fields = ['data_prescricao']
    raw_id_fields = ['atendimento', 'profissional']
    inlines = [ItemPrescricaoInline]

    fieldsets = (
        ('Atendimento', {
            'fields': ('atendimento', 'profissional')
        }),
        ('Prescrição', {
            'fields': ('validade', 'status', 'observacoes')
        }),
        ('Informações de Sistema', {
            'fields': ('data_prescricao',),
            'classes': ('collapse',)
        }),
    )

    def total_itens(self, obj):
        """Exibe total de medicamentos prescritos"""
        return obj.total_itens()
    total_itens.short_description = 'Total de Medicamentos'

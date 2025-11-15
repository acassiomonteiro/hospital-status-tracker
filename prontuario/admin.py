from django.contrib import admin
from .models import Evolucao, SinalVital, Prescricao, ItemPrescricao, SolicitacaoExame, ResultadoExame


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


@admin.register(SolicitacaoExame)
class SolicitacaoExameAdmin(admin.ModelAdmin):
    list_display = ['nome_exame', 'tipo', 'atendimento', 'profissional', 'status', 'data_solicitacao', 'tem_resultado_admin']
    list_filter = ['tipo', 'status', 'data_solicitacao', 'profissional']
    search_fields = ['nome_exame', 'atendimento__paciente__nome', 'justificativa', 'profissional__user__username']
    readonly_fields = ['data_solicitacao', 'data_atualizacao']
    raw_id_fields = ['atendimento', 'profissional']

    fieldsets = (
        ('Atendimento', {
            'fields': ('atendimento', 'profissional')
        }),
        ('Exame', {
            'fields': ('tipo', 'nome_exame', 'justificativa')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Informações de Sistema', {
            'fields': ('data_solicitacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def tem_resultado_admin(self, obj):
        """Exibe se a solicitação possui resultado"""
        if obj.tem_resultado():
            return '✅ Sim'
        return '❌ Não'
    tem_resultado_admin.short_description = 'Possui Resultado'


@admin.register(ResultadoExame)
class ResultadoExameAdmin(admin.ModelAdmin):
    list_display = ['solicitacao', 'data_resultado', 'tem_arquivo']
    list_filter = ['data_resultado']
    search_fields = ['solicitacao__nome_exame', 'resultado_texto', 'observacoes']
    readonly_fields = ['data_resultado']
    raw_id_fields = ['solicitacao']

    fieldsets = (
        ('Solicitação', {
            'fields': ('solicitacao',)
        }),
        ('Resultado', {
            'fields': ('resultado_texto', 'arquivo_laudo', 'observacoes')
        }),
        ('Informações de Sistema', {
            'fields': ('data_resultado',),
            'classes': ('collapse',)
        }),
    )

    def tem_arquivo(self, obj):
        """Exibe se o resultado possui arquivo anexo"""
        if obj.arquivo_laudo:
            return '✅ Sim'
        return '❌ Não'
    tem_arquivo.short_description = 'Possui Laudo Anexo'

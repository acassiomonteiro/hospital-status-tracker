from django.urls import path
from . import views

urlpatterns = [
    # Evoluções Clínicas
    path('atendimento/<int:atendimento_id>/evolucoes/', views.EvolucoesAtendimentoView.as_view(), name='evolucoes_atendimento'),
    path('atendimento/<int:atendimento_id>/evolucao/nova/', views.NovaEvolucaoView.as_view(), name='nova_evolucao'),

    # Sinais Vitais
    path('atendimento/<int:atendimento_id>/sinais-vitais/', views.SinaisVitaisAtendimentoView.as_view(), name='sinais_vitais_atendimento'),
    path('atendimento/<int:atendimento_id>/sinais-vitais/novo/', views.NovoSinalVitalView.as_view(), name='novo_sinal_vital'),

    # Prescrições Médicas
    path('atendimento/<int:atendimento_id>/prescricoes/', views.PrescricoesAtendimentoView.as_view(), name='prescricoes_atendimento'),
    path('atendimento/<int:atendimento_id>/prescricao/nova/', views.NovaPrescricaoView.as_view(), name='nova_prescricao'),

    # Exames
    path('atendimento/<int:atendimento_id>/exames/', views.SolicitacoesExameAtendimentoView.as_view(), name='solicitacoes_exame_atendimento'),
    path('atendimento/<int:atendimento_id>/exame/solicitar/', views.NovaSolicitacaoExameView.as_view(), name='nova_solicitacao_exame'),
    path('exame/<int:solicitacao_id>/resultado/', views.AdicionarResultadoExameView.as_view(), name='adicionar_resultado_exame'),
    path('exame/<int:solicitacao_id>/cancelar/', views.CancelarExameView.as_view(), name='cancelar_exame'),
]

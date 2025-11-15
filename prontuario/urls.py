from django.urls import path
from . import views

urlpatterns = [
    # Evoluções Clínicas
    path('atendimento/<int:atendimento_id>/evolucoes/', views.EvolucoesAtendimentoView.as_view(), name='evolucoes_atendimento'),
    path('atendimento/<int:atendimento_id>/evolucao/nova/', views.NovaEvolucaoView.as_view(), name='nova_evolucao'),

    # Sinais Vitais
    path('atendimento/<int:atendimento_id>/sinais-vitais/', views.SinaisVitaisAtendimentoView.as_view(), name='sinais_vitais_atendimento'),
    path('atendimento/<int:atendimento_id>/sinais-vitais/novo/', views.NovoSinalVitalView.as_view(), name='novo_sinal_vital'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('atendimento/<int:atendimento_id>/evolucoes/', views.EvolucoesAtendimentoView.as_view(), name='evolucoes_atendimento'),
    path('atendimento/<int:atendimento_id>/evolucao/nova/', views.NovaEvolucaoView.as_view(), name='nova_evolucao'),
]

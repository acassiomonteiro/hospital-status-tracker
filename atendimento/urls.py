from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('novo/', views.NovoAtendimentoView.as_view(), name='novo_atendimento'),
    path('atualizar/<int:atendimento_id>/', views.AtualizarStatusView.as_view(), name='atualizar_status'),
]

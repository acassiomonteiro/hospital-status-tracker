from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Atendimentos
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('novo/', views.NovoAtendimentoView.as_view(), name='novo_atendimento'),
    path('atualizar/<int:atendimento_id>/', views.AtualizarStatusView.as_view(), name='atualizar_status'),
]

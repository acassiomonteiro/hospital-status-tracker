from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('novo/', views.novo_atendimento, name='novo_atendimento'),
    path('atualizar/<int:atendimento_id>/', views.atualizar_status, name='atualizar_status'),
]

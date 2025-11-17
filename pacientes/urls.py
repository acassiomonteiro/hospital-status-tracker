from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.BuscarPacienteView.as_view(), name='buscar_paciente'),
]

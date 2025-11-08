from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'criado_em']
    search_fields = ['nome', 'cpf']
    list_filter = ['criado_em']
    readonly_fields = ['criado_em']

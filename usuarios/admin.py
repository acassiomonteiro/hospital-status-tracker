from django.contrib import admin
from .models import Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['user', 'perfil', 'registro_profissional', 'criado_em']
    list_filter = ['perfil', 'criado_em']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'registro_profissional']
    readonly_fields = ['criado_em']
    raw_id_fields = ['user']

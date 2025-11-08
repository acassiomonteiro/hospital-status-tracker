from django.db import models
from django.contrib.auth.models import User


class Profissional(models.Model):
    """Model para profissionais de saúde com perfis de acesso"""

    PERFIL_CHOICES = [
        ('MEDICO', 'Médico'),
        ('ENFERMEIRO', 'Enfermeiro'),
        ('ADMINISTRATIVO', 'Administrativo'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profissional',
        verbose_name='Usuário'
    )
    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        verbose_name='Perfil de Acesso'
    )
    registro_profissional = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Registro Profissional',
        help_text='CRM, COREN ou outro registro'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        nome_completo = self.user.get_full_name() or self.user.username
        return f"{nome_completo} - {self.get_perfil_display()}"

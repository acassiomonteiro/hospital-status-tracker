from django.db import models
from atendimentos.models import Atendimento
from usuarios.models import Profissional


class Evolucao(models.Model):
    """Model para registro de evoluções clínicas durante o atendimento"""

    TIPO_CHOICES = [
        ('ANAMNESE', 'Anamnese'),
        ('EVOLUCAO_MEDICA', 'Evolução Médica'),
        ('EVOLUCAO_ENFERMAGEM', 'Evolução de Enfermagem'),
        ('EXAME_FISICO', 'Exame Físico'),
    ]

    atendimento = models.ForeignKey(
        Atendimento,
        on_delete=models.PROTECT,
        related_name='evolucoes',
        verbose_name='Atendimento'
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='evolucoes',
        verbose_name='Profissional'
    )
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Evolução'
    )
    descricao = models.TextField(verbose_name='Descrição')
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora'
    )

    class Meta:
        verbose_name = 'Evolução Clínica'
        verbose_name_plural = 'Evoluções Clínicas'
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.atendimento.paciente.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def get_tipo_badge_class(self):
        """Retorna classe CSS para estilizar o tipo de evolução"""
        tipo_classes = {
            'ANAMNESE': 'bg-cyan-100 text-cyan-800 border-cyan-300',
            'EVOLUCAO_MEDICA': 'bg-blue-100 text-blue-800 border-blue-300',
            'EVOLUCAO_ENFERMAGEM': 'bg-green-100 text-green-800 border-green-300',
            'EXAME_FISICO': 'bg-purple-100 text-purple-800 border-purple-300',
        }
        return tipo_classes.get(self.tipo, 'bg-gray-100 text-gray-800 border-gray-300')

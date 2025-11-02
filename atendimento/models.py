from django.db import models
from django.core.validators import RegexValidator


class Paciente(models.Model):
    """Model para armazenar dados básicos do paciente"""

    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='CPF',
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='CPF deve conter exatamente 11 dígitos numéricos',
            )
        ]
    )
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"


class Atendimento(models.Model):
    """Model para registrar atendimentos no pronto-socorro"""

    STATUS_CHOICES = [
        ('TRIAGEM', 'Triagem'),
        ('EM_ATENDIMENTO', 'Em Atendimento'),
        ('AGUARDANDO_EXAME', 'Aguardando Exame'),
        ('EM_EXAME', 'Em Exame'),
        ('AGUARDANDO_RESULTADO', 'Aguardando Resultado'),
        ('ALTA', 'Alta'),
        ('INTERNACAO', 'Internação'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='atendimentos',
        verbose_name='Paciente'
    )
    data_hora_entrada = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora Entrada'
    )
    queixa = models.TextField(verbose_name='Queixa Principal')
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='TRIAGEM',
        verbose_name='Status'
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'
        ordering = ['-data_hora_entrada']

    def __str__(self):
        return f"{self.paciente.nome} - {self.get_status_display()} - {self.data_hora_entrada.strftime('%d/%m/%Y %H:%M')}"

    def get_status_badge_class(self):
        """Retorna classe CSS para estilizar o status"""
        status_classes = {
            'TRIAGEM': 'bg-yellow-100 text-yellow-800',
            'EM_ATENDIMENTO': 'bg-blue-100 text-blue-800',
            'AGUARDANDO_EXAME': 'bg-purple-100 text-purple-800',
            'EM_EXAME': 'bg-indigo-100 text-indigo-800',
            'AGUARDANDO_RESULTADO': 'bg-orange-100 text-orange-800',
            'ALTA': 'bg-green-100 text-green-800',
            'INTERNACAO': 'bg-red-100 text-red-800',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')

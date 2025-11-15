from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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


class SinalVital(models.Model):
    """Model para registro de sinais vitais durante o atendimento"""

    atendimento = models.ForeignKey(
        Atendimento,
        on_delete=models.PROTECT,
        related_name='sinais_vitais',
        verbose_name='Atendimento'
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='sinais_vitais_registrados',
        verbose_name='Profissional'
    )

    # Pressão Arterial (mmHg)
    pressao_arterial_sistolica = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        verbose_name='Pressão Arterial Sistólica (mmHg)',
        help_text='Valor entre 50 e 300 mmHg'
    )
    pressao_arterial_diastolica = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        verbose_name='Pressão Arterial Diastólica (mmHg)',
        help_text='Valor entre 30 e 200 mmHg'
    )

    # Frequência Cardíaca (bpm)
    frequencia_cardiaca = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(250)],
        verbose_name='Frequência Cardíaca (bpm)',
        help_text='Valor entre 30 e 250 bpm'
    )

    # Frequência Respiratória (irpm)
    frequencia_respiratoria = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(8), MaxValueValidator(60)],
        verbose_name='Frequência Respiratória (irpm)',
        help_text='Valor entre 8 e 60 irpm'
    )

    # Temperatura (°C)
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(32.0), MaxValueValidator(45.0)],
        verbose_name='Temperatura (°C)',
        help_text='Valor entre 32.0 e 45.0 °C'
    )

    # Saturação de O2 (%)
    saturacao_o2 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        verbose_name='Saturação de O₂ (%)',
        help_text='Valor entre 50 e 100%'
    )

    # Glicemia (mg/dL)
    glicemia = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(600)],
        verbose_name='Glicemia (mg/dL)',
        help_text='Valor entre 20 e 600 mg/dL'
    )

    # Observações adicionais
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Informações adicionais sobre a aferição'
    )

    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora'
    )

    class Meta:
        verbose_name = 'Sinal Vital'
        verbose_name_plural = 'Sinais Vitais'
        ordering = ['-data_hora']

    def __str__(self):
        return f"Sinais Vitais - {self.atendimento.paciente.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def get_pressao_arterial(self):
        """Retorna pressão arterial formatada (ex: 120/80)"""
        if self.pressao_arterial_sistolica and self.pressao_arterial_diastolica:
            return f"{self.pressao_arterial_sistolica}/{self.pressao_arterial_diastolica}"
        return "Não aferida"

    def tem_sinais_alterados(self):
        """Verifica se algum sinal vital está fora dos parâmetros normais"""
        alertas = []

        # Pressão arterial
        if self.pressao_arterial_sistolica and self.pressao_arterial_sistolica > 140:
            alertas.append('Pressão sistólica elevada')
        if self.pressao_arterial_diastolica and self.pressao_arterial_diastolica > 90:
            alertas.append('Pressão diastólica elevada')

        # Frequência cardíaca
        if self.frequencia_cardiaca:
            if self.frequencia_cardiaca < 60:
                alertas.append('Bradicardia')
            elif self.frequencia_cardiaca > 100:
                alertas.append('Taquicardia')

        # Temperatura
        if self.temperatura:
            if self.temperatura < 36.0:
                alertas.append('Hipotermia')
            elif self.temperatura > 37.5:
                alertas.append('Febre')

        # Saturação O2
        if self.saturacao_o2 and self.saturacao_o2 < 95:
            alertas.append('Saturação baixa')

        return alertas


class Prescricao(models.Model):
    """Model para registro de prescrições médicas durante o atendimento"""

    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('SUSPENSA', 'Suspensa'),
        ('CONCLUIDA', 'Concluída'),
    ]

    atendimento = models.ForeignKey(
        Atendimento,
        on_delete=models.PROTECT,
        related_name='prescricoes',
        verbose_name='Atendimento'
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='prescricoes_realizadas',
        verbose_name='Médico Responsável'
    )
    data_prescricao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Prescrição'
    )
    validade = models.DateField(
        verbose_name='Validade',
        help_text='Data até quando a prescrição é válida'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ATIVA',
        verbose_name='Status'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações Gerais',
        help_text='Observações sobre a prescrição (opcional)'
    )

    class Meta:
        verbose_name = 'Prescrição Médica'
        verbose_name_plural = 'Prescrições Médicas'
        ordering = ['-data_prescricao']

    def __str__(self):
        return f"Prescrição - {self.atendimento.paciente.nome} - {self.data_prescricao.strftime('%d/%m/%Y %H:%M')}"

    def get_status_badge_class(self):
        """Retorna classe CSS para estilizar o status da prescrição"""
        status_classes = {
            'ATIVA': 'bg-green-100 text-green-800 border-green-300',
            'SUSPENSA': 'bg-yellow-100 text-yellow-800 border-yellow-300',
            'CONCLUIDA': 'bg-gray-100 text-gray-800 border-gray-300',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800 border-gray-300')

    def total_itens(self):
        """Retorna o total de medicamentos prescritos"""
        return self.itens.count()


class ItemPrescricao(models.Model):
    """Model para itens individuais de uma prescrição (medicamentos)"""

    VIA_CHOICES = [
        ('ORAL', 'Oral'),
        ('INTRAVENOSA', 'Intravenosa (IV)'),
        ('INTRAMUSCULAR', 'Intramuscular (IM)'),
        ('SUBCUTANEA', 'Subcutânea (SC)'),
        ('TOPICA', 'Tópica'),
        ('INALATORIA', 'Inalatória'),
        ('SUBLINGUAL', 'Sublingual'),
        ('RETAL', 'Retal'),
        ('OCULAR', 'Ocular'),
        ('NASAL', 'Nasal'),
    ]

    prescricao = models.ForeignKey(
        'Prescricao',
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Prescrição'
    )
    medicamento = models.CharField(
        max_length=200,
        verbose_name='Medicamento',
        help_text='Nome do medicamento'
    )
    dose = models.CharField(
        max_length=100,
        verbose_name='Dose',
        help_text='Ex: 500mg, 10ml, 2 comprimidos'
    )
    via = models.CharField(
        max_length=20,
        choices=VIA_CHOICES,
        verbose_name='Via de Administração'
    )
    frequencia = models.CharField(
        max_length=100,
        verbose_name='Frequência',
        help_text='Ex: 8/8h, 12/12h, 1x ao dia'
    )
    duracao_dias = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        verbose_name='Duração (dias)',
        help_text='Quantidade de dias do tratamento'
    )
    observacoes_item = models.TextField(
        blank=True,
        verbose_name='Observações do Item',
        help_text='Instruções específicas para este medicamento (opcional)'
    )

    class Meta:
        verbose_name = 'Item da Prescrição'
        verbose_name_plural = 'Itens da Prescrição'
        ordering = ['id']

    def __str__(self):
        return f"{self.medicamento} - {self.dose} - {self.get_via_display()}"

from django.db import models
from django.core.validators import RegexValidator


class Paciente(models.Model):
    """Model para armazenar dados completos do paciente (prontuário eletrônico)"""

    # Choices
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    TIPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # Dados Básicos (obrigatórios - compatibilidade retroativa)
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

    # Dados Pessoais (opcionais)
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Sexo'
    )
    nome_mae = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nome da Mãe'
    )
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\d{10,11}$',
                message='Telefone deve conter 10 ou 11 dígitos (incluindo DDD)',
            )
        ],
        help_text='Somente números (DDD + número)'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='E-mail'
    )

    # Documentos (opcionais)
    cartao_sus = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Cartão SUS',
        validators=[
            RegexValidator(
                regex=r'^\d{15}$',
                message='Cartão SUS deve conter exatamente 15 dígitos',
            )
        ]
    )
    rg = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='RG'
    )

    # Endereço (opcionais)
    cep = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name='CEP',
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='CEP deve conter exatamente 8 dígitos',
            )
        ],
        help_text='Somente números'
    )
    rua = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Rua/Avenida'
    )
    numero = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Número'
    )
    bairro = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Bairro'
    )
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Cidade'
    )
    uf = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name='UF',
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}$',
                message='UF deve conter exatamente 2 letras maiúsculas',
            )
        ]
    )

    # Dados Clínicos (opcionais)
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=TIPO_SANGUINEO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Tipo Sanguíneo'
    )
    alergias = models.TextField(
        blank=True,
        null=True,
        verbose_name='Alergias',
        help_text='Liste medicamentos, alimentos ou outras substâncias'
    )
    observacoes_clinicas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações Clínicas',
        help_text='Doenças pré-existentes, cirurgias anteriores, etc.'
    )

    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"

    def get_endereco_completo(self):
        """Retorna o endereço completo formatado"""
        partes = []
        if self.rua:
            partes.append(self.rua)
        if self.numero:
            partes.append(f"nº {self.numero}")
        if self.bairro:
            partes.append(self.bairro)
        if self.cidade and self.uf:
            partes.append(f"{self.cidade}/{self.uf}")
        elif self.cidade:
            partes.append(self.cidade)

        return ', '.join(partes) if partes else 'Não informado'

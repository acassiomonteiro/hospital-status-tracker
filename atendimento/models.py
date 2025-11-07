from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


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
    profissional_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='atendimentos',
        verbose_name='Profissional Responsável',
        null=True,
        blank=True
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

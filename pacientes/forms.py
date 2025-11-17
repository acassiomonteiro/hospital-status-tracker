from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):
    """Formulário para cadastro completo de paciente (prontuário eletrônico)"""

    class Meta:
        model = Paciente
        fields = [
            # Dados Básicos
            'nome', 'cpf', 'data_nascimento',
            # Dados Pessoais
            'sexo', 'nome_mae', 'telefone', 'email',
            # Documentos
            'cartao_sus', 'rg',
            # Endereço
            'cep', 'rua', 'numero', 'bairro', 'cidade', 'uf',
            # Dados Clínicos
            'tipo_sanguineo', 'alergias', 'observacoes_clinicas'
        ]

        # Classes CSS padrão
        _input_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'

        widgets = {
            # Dados Básicos
            'nome': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Nome completo do paciente'
            }),
            'cpf': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Somente números (11 dígitos)',
                'maxlength': '11'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': _input_class,
                'type': 'date'
            }),

            # Dados Pessoais
            'sexo': forms.Select(attrs={
                'class': _input_class
            }),
            'nome_mae': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Nome completo da mãe'
            }),
            'telefone': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': '(DDD) + número (somente números)',
                'maxlength': '11'
            }),
            'email': forms.EmailInput(attrs={
                'class': _input_class,
                'placeholder': 'exemplo@email.com'
            }),

            # Documentos
            'cartao_sus': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Somente números (15 dígitos)',
                'maxlength': '15'
            }),
            'rg': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Número do RG'
            }),

            # Endereço
            'cep': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Somente números (8 dígitos)',
                'maxlength': '8'
            }),
            'rua': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Rua, avenida, travessa...'
            }),
            'numero': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Número ou S/N'
            }),
            'bairro': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Cidade'
            }),
            'uf': forms.TextInput(attrs={
                'class': _input_class,
                'placeholder': 'Ex: MG, SP, RJ',
                'maxlength': '2',
                'style': 'text-transform: uppercase;'
            }),

            # Dados Clínicos
            'tipo_sanguineo': forms.Select(attrs={
                'class': _input_class
            }),
            'alergias': forms.Textarea(attrs={
                'class': _input_class,
                'placeholder': 'Liste medicamentos, alimentos ou outras substâncias às quais o paciente é alérgico',
                'rows': 3
            }),
            'observacoes_clinicas': forms.Textarea(attrs={
                'class': _input_class,
                'placeholder': 'Doenças pré-existentes, cirurgias anteriores, medicamentos de uso contínuo, etc.',
                'rows': 3
            }),
        }

    def clean_cpf(self):
        """Remove caracteres não numéricos do CPF"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
        return cpf

    def clean_telefone(self):
        """Remove caracteres não numéricos do telefone"""
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = ''.join(filter(str.isdigit, telefone))
        return telefone

    def clean_cep(self):
        """Remove caracteres não numéricos do CEP"""
        cep = self.cleaned_data.get('cep')
        if cep:
            cep = ''.join(filter(str.isdigit, cep))
        return cep

    def clean_cartao_sus(self):
        """Remove caracteres não numéricos do Cartão SUS"""
        cartao_sus = self.cleaned_data.get('cartao_sus')
        if cartao_sus:
            cartao_sus = ''.join(filter(str.isdigit, cartao_sus))
        return cartao_sus

    def clean_uf(self):
        """Converte UF para maiúsculas"""
        uf = self.cleaned_data.get('uf')
        if uf:
            uf = uf.upper()
        return uf


class PacienteBuscaForm(forms.Form):
    """Formulário para busca avançada de pacientes"""

    cpf = forms.CharField(
        max_length=11,
        required=False,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Digite o CPF (parcial ou completo)',
            'maxlength': '11'
        })
    )

    nome = forms.CharField(
        max_length=200,
        required=False,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Digite o nome ou parte dele'
        })
    )

    data_nascimento = forms.DateField(
        required=False,
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'type': 'date'
        })
    )

    def clean_cpf(self):
        """Remove caracteres não numéricos do CPF"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
        return cpf

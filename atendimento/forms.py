from django import forms
from .models import Paciente, Atendimento


class PacienteForm(forms.ModelForm):
    """Formulário para cadastro de paciente"""

    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Nome completo do paciente'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Somente números (11 dígitos)',
                'maxlength': '11'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Remove qualquer caracter não numérico
        cpf = ''.join(filter(str.isdigit, cpf))
        return cpf


class AtendimentoForm(forms.ModelForm):
    """Formulário para registro de atendimento"""

    class Meta:
        model = Atendimento
        fields = ['queixa', 'status']
        widgets = {
            'queixa': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Descreva a queixa principal do paciente',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
        }

from django import forms
from .models import Atendimento
from usuarios.models import Profissional


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


class AtendimentoBuscaForm(forms.Form):
    """Formulário para busca e filtragem de atendimentos"""

    status = forms.ChoiceField(
        choices=[('', 'Todos os Status')] + Atendimento.STATUS_CHOICES,
        required=False,
        label='Status',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )

    profissional_responsavel = forms.ModelChoiceField(
        queryset=Profissional.objects.select_related('user').all(),
        required=False,
        label='Profissional Responsável',
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )

    data_inicio = forms.DateField(
        required=False,
        label='Data Inicial',
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'type': 'date'
        })
    )

    data_fim = forms.DateField(
        required=False,
        label='Data Final',
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'type': 'date'
        })
    )

    paciente_nome = forms.CharField(
        max_length=200,
        required=False,
        label='Nome do Paciente',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Digite o nome do paciente'
        })
    )

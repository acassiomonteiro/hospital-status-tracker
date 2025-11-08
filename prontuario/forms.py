from django import forms
from .models import Evolucao


class EvolucaoForm(forms.ModelForm):
    """Formulário para registro rápido de evolução clínica"""

    class Meta:
        model = Evolucao
        fields = ['tipo', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Descreva a evolução clínica do paciente...',
                'rows': 8
            }),
        }

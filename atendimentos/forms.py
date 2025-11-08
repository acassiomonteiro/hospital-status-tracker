from django import forms
from .models import Atendimento


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

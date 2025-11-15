from django import forms
from django.core.exceptions import ValidationError
from .models import Evolucao, SinalVital


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


class SinalVitalForm(forms.ModelForm):
    """Formulário para registro rápido de sinais vitais"""

    class Meta:
        model = SinalVital
        fields = [
            'pressao_arterial_sistolica',
            'pressao_arterial_diastolica',
            'frequencia_cardiaca',
            'frequencia_respiratoria',
            'temperatura',
            'saturacao_o2',
            'glicemia',
            'observacoes'
        ]
        widgets = {
            'pressao_arterial_sistolica': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 120',
                'min': '50',
                'max': '300'
            }),
            'pressao_arterial_diastolica': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 80',
                'min': '30',
                'max': '200'
            }),
            'frequencia_cardiaca': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 72',
                'min': '30',
                'max': '250'
            }),
            'frequencia_respiratoria': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 16',
                'min': '8',
                'max': '60'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 36.5',
                'step': '0.1',
                'min': '32.0',
                'max': '45.0'
            }),
            'saturacao_o2': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 98',
                'min': '50',
                'max': '100'
            }),
            'glicemia': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 95',
                'min': '20',
                'max': '600'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Observações sobre a aferição (opcional)...',
                'rows': 3
            }),
        }

    def clean(self):
        """Validação customizada para garantir coerência dos dados"""
        cleaned_data = super().clean()

        # Verifica se ao menos um sinal vital foi preenchido
        campos_vitais = [
            'pressao_arterial_sistolica',
            'pressao_arterial_diastolica',
            'frequencia_cardiaca',
            'frequencia_respiratoria',
            'temperatura',
            'saturacao_o2',
            'glicemia'
        ]

        tem_algum_valor = any(cleaned_data.get(campo) for campo in campos_vitais)

        if not tem_algum_valor:
            raise ValidationError(
                'É necessário preencher ao menos um sinal vital.'
            )

        # Valida pressão arterial (se uma está preenchida, a outra também deve estar)
        sistolica = cleaned_data.get('pressao_arterial_sistolica')
        diastolica = cleaned_data.get('pressao_arterial_diastolica')

        if (sistolica and not diastolica) or (diastolica and not sistolica):
            raise ValidationError(
                'Para registrar pressão arterial, preencha tanto a sistólica quanto a diastólica.'
            )

        # Valida coerência da pressão arterial (sistólica deve ser maior que diastólica)
        if sistolica and diastolica and sistolica <= diastolica:
            raise ValidationError(
                'A pressão sistólica deve ser maior que a diastólica.'
            )

        return cleaned_data

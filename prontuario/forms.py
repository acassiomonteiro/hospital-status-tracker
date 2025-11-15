from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from datetime import date, timedelta
from .models import Evolucao, SinalVital, Prescricao, ItemPrescricao, SolicitacaoExame, ResultadoExame


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


class PrescricaoForm(forms.ModelForm):
    """Formulário para registro de prescrição médica"""

    class Meta:
        model = Prescricao
        fields = ['validade', 'observacoes']
        widgets = {
            'validade': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Observações gerais sobre a prescrição (opcional)...',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define validade padrão para 7 dias à frente
        if not self.instance.pk:
            self.fields['validade'].initial = date.today() + timedelta(days=7)

    def clean_validade(self):
        """Valida que a validade não é anterior à data atual"""
        validade = self.cleaned_data.get('validade')
        if validade and validade < date.today():
            raise ValidationError('A validade não pode ser anterior à data atual.')
        return validade


class ItemPrescricaoForm(forms.ModelForm):
    """Formulário para itens individuais da prescrição"""

    class Meta:
        model = ItemPrescricao
        fields = ['medicamento', 'dose', 'via', 'frequencia', 'duracao_dias', 'observacoes_item']
        widgets = {
            'medicamento': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Dipirona 500mg'
            }),
            'dose': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 1 comprimido, 10ml'
            }),
            'via': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            }),
            'frequencia': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 8/8h, 12/12h, 1x ao dia'
            }),
            'duracao_dias': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: 7',
                'min': '1',
                'max': '365'
            }),
            'observacoes_item': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Instruções específicas (opcional)...',
                'rows': 2
            }),
        }


# FormSet para permitir múltiplos medicamentos em uma prescrição
ItemPrescricaoFormSet = inlineformset_factory(
    Prescricao,
    ItemPrescricao,
    form=ItemPrescricaoForm,
    extra=1,  # Começa com 1 formulário vazio
    min_num=1,  # Requer ao menos 1 medicamento
    validate_min=True,
    can_delete=True
)


class SolicitacaoExameForm(forms.ModelForm):
    """Formulário para solicitação de exames"""

    class Meta:
        model = SolicitacaoExame
        fields = ['tipo', 'nome_exame', 'justificativa']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            }),
            'nome_exame': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Hemograma completo, Raio-X de tórax'
            }),
            'justificativa': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Descreva a justificativa clínica para a solicitação deste exame...',
                'rows': 4
            }),
        }


class ResultadoExameForm(forms.ModelForm):
    """Formulário para registro de resultado de exame"""

    class Meta:
        model = ResultadoExame
        fields = ['resultado_texto', 'arquivo_laudo', 'observacoes']
        widgets = {
            'resultado_texto': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Descreva o resultado do exame...',
                'rows': 6
            }),
            'arquivo_laudo': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Observações adicionais sobre o resultado (opcional)...',
                'rows': 3
            }),
        }

    def clean_arquivo_laudo(self):
        """Valida o tipo e tamanho do arquivo enviado"""
        arquivo = self.cleaned_data.get('arquivo_laudo')

        if arquivo:
            # Valida extensão do arquivo
            extensoes_validas = ['.pdf', '.jpg', '.jpeg', '.png']
            nome_arquivo = arquivo.name.lower()
            if not any(nome_arquivo.endswith(ext) for ext in extensoes_validas):
                raise ValidationError(
                    'Apenas arquivos PDF e imagens (JPG, PNG) são permitidos.'
                )

            # Valida tamanho (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB em bytes
            if arquivo.size > max_size:
                raise ValidationError(
                    'O arquivo não pode exceder 10MB.'
                )

        return arquivo

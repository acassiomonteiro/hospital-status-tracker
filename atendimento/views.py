from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Paciente, Atendimento
from .forms import PacienteForm, AtendimentoForm


def dashboard(request):
    """View principal - lista todos os atendimentos"""
    atendimentos = Atendimento.objects.select_related('paciente').all()
    context = {
        'atendimentos': atendimentos,
        'total_atendimentos': atendimentos.count(),
    }
    return render(request, 'atendimento/dashboard.html', context)


def novo_atendimento(request):
    """View para criar novo paciente + atendimento"""
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)
        atendimento_form = AtendimentoForm(request.POST)

        if paciente_form.is_valid() and atendimento_form.is_valid():
            # Verifica se paciente já existe pelo CPF
            cpf = paciente_form.cleaned_data['cpf']
            paciente, created = Paciente.objects.get_or_create(
                cpf=cpf,
                defaults={
                    'nome': paciente_form.cleaned_data['nome'],
                    'data_nascimento': paciente_form.cleaned_data['data_nascimento']
                }
            )

            # Cria o atendimento
            atendimento = atendimento_form.save(commit=False)
            atendimento.paciente = paciente
            atendimento.save()

            if created:
                messages.success(request, f'Paciente {paciente.nome} cadastrado e atendimento registrado com sucesso!')
            else:
                messages.success(request, f'Novo atendimento registrado para {paciente.nome}!')

            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao salvar. Verifique os dados informados.')
    else:
        paciente_form = PacienteForm()
        atendimento_form = AtendimentoForm()

    context = {
        'paciente_form': paciente_form,
        'atendimento_form': atendimento_form,
    }
    return render(request, 'atendimento/novo_atendimento.html', context)


def atualizar_status(request, atendimento_id):
    """View para atualizar status de um atendimento"""
    atendimento = get_object_or_404(Atendimento, pk=atendimento_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status:
            atendimento.status = novo_status
            atendimento.save()
            messages.success(request, f'Status atualizado para: {atendimento.get_status_display()}')
        return redirect('dashboard')

    context = {
        'atendimento': atendimento,
        'status_choices': Atendimento.STATUS_CHOICES,
    }
    return render(request, 'atendimento/atualizar_status.html', context)

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DetailView
from django.urls import reverse_lazy
from pacientes.models import Paciente
from pacientes.forms import PacienteForm
from usuarios.models import Profissional
from .models import Atendimento
from .forms import AtendimentoForm


class DashboardView(LoginRequiredMixin, ListView):
    """View principal - lista todos os atendimentos"""
    model = Atendimento
    template_name = 'atendimento/dashboard.html'
    context_object_name = 'atendimentos'

    def get_queryset(self):
        """Retorna queryset otimizado com select_related"""
        return Atendimento.objects.select_related('paciente', 'profissional_responsavel__user').all()

    def get_context_data(self, **kwargs):
        """Adiciona total de atendimentos ao contexto"""
        context = super().get_context_data(**kwargs)
        context['total_atendimentos'] = self.get_queryset().count()
        return context


class NovoAtendimentoView(LoginRequiredMixin, FormView):
    """View para criar novo paciente + atendimento (multi-form)"""
    template_name = 'atendimento/novo_atendimento.html'
    success_url = reverse_lazy('dashboard')
    form_class = None  # Não usamos form_class padrão pois temos múltiplos forms

    def get(self, request, *args, **kwargs):
        """Handler GET - renderiza formulários vazios"""
        context = {
            'paciente_form': PacienteForm(),
            'atendimento_form': AtendimentoForm(),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """Processa os dois forms simultaneamente"""
        paciente_form = PacienteForm(request.POST)
        atendimento_form = AtendimentoForm(request.POST)

        if paciente_form.is_valid() and atendimento_form.is_valid():
            return self.forms_valid(paciente_form, atendimento_form)
        else:
            messages.error(request, 'Erro ao salvar. Verifique os dados informados.')
            return self.render_to_response({
                'paciente_form': paciente_form,
                'atendimento_form': atendimento_form,
            })

    def forms_valid(self, paciente_form, atendimento_form):
        """Processa os forms válidos e cria paciente + atendimento"""
        # Verifica se paciente já existe pelo CPF (get_or_create)
        cpf = paciente_form.cleaned_data['cpf']
        paciente, created = Paciente.objects.get_or_create(
            cpf=cpf,
            defaults={
                'nome': paciente_form.cleaned_data['nome'],
                'data_nascimento': paciente_form.cleaned_data['data_nascimento']
            }
        )

        # Cria o atendimento vinculado ao paciente e profissional
        atendimento = atendimento_form.save(commit=False)
        atendimento.paciente = paciente

        # Vincula o profissional responsável (usuário logado)
        try:
            atendimento.profissional_responsavel = self.request.user.profissional
        except Profissional.DoesNotExist:
            messages.warning(
                self.request,
                'Atenção: Seu usuário não possui perfil de profissional vinculado.'
            )

        atendimento.save()

        # Mensagem de sucesso condicional
        if created:
            messages.success(
                self.request,
                f'Paciente {paciente.nome} cadastrado e atendimento registrado com sucesso!'
            )
        else:
            messages.success(
                self.request,
                f'Novo atendimento registrado para {paciente.nome}!'
            )

        return redirect(self.success_url)


class AtualizarStatusView(LoginRequiredMixin, DetailView):
    """View para atualizar status de um atendimento"""
    model = Atendimento
    template_name = 'atendimento/atualizar_status.html'
    pk_url_kwarg = 'atendimento_id'
    context_object_name = 'atendimento'

    def get_context_data(self, **kwargs):
        """Adiciona choices de status ao contexto"""
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Atendimento.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        """Processa atualização de status via POST direto"""
        atendimento = self.get_object()
        novo_status = request.POST.get('status')

        if novo_status:
            atendimento.status = novo_status
            atendimento.save()
            messages.success(
                request,
                f'Status atualizado para: {atendimento.get_status_display()}'
            )

        return redirect('dashboard')

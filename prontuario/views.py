from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView
from django.urls import reverse
from atendimentos.models import Atendimento
from usuarios.models import Profissional
from .models import Evolucao
from .forms import EvolucaoForm


class NovaEvolucaoView(LoginRequiredMixin, FormView):
    """View para adicionar nova evolução clínica a um atendimento"""
    template_name = 'atendimento/nova_evolucao.html'
    form_class = EvolucaoForm

    def get_success_url(self):
        """Retorna para a timeline de evoluções do atendimento"""
        return reverse('evolucoes_atendimento', kwargs={'atendimento_id': self.kwargs['atendimento_id']})

    def get_context_data(self, **kwargs):
        """Adiciona atendimento ao contexto"""
        context = super().get_context_data(**kwargs)
        atendimento = get_object_or_404(
            Atendimento.objects.select_related('paciente'),
            pk=self.kwargs['atendimento_id']
        )
        context['atendimento'] = atendimento
        return context

    def form_valid(self, form):
        """Salva evolução vinculando atendimento e profissional automaticamente"""
        evolucao = form.save(commit=False)

        # Vincula atendimento
        evolucao.atendimento = get_object_or_404(Atendimento, pk=self.kwargs['atendimento_id'])

        # Vincula profissional logado
        try:
            evolucao.profissional = self.request.user.profissional
        except Profissional.DoesNotExist:
            messages.error(
                self.request,
                'Erro: Seu usuário não possui perfil de profissional vinculado.'
            )
            return redirect('dashboard')

        evolucao.save()

        messages.success(
            self.request,
            f'Evolução registrada com sucesso: {evolucao.get_tipo_display()}'
        )

        return super().form_valid(form)


class EvolucoesAtendimentoView(LoginRequiredMixin, DetailView):
    """View para listar timeline de evoluções de um atendimento"""
    model = Atendimento
    template_name = 'atendimento/evolucoes_atendimento.html'
    pk_url_kwarg = 'atendimento_id'
    context_object_name = 'atendimento'

    def get_queryset(self):
        """Otimiza query com prefetch de evoluções"""
        return Atendimento.objects.select_related(
            'paciente',
            'profissional_responsavel__user'
        ).prefetch_related(
            'evolucoes__profissional__user'
        )

    def get_context_data(self, **kwargs):
        """Adiciona evoluções ao contexto (ordem cronológica reversa)"""
        context = super().get_context_data(**kwargs)
        context['evolucoes'] = self.object.evolucoes.select_related(
            'profissional__user'
        ).all()  # Já ordenado por -data_hora no Model Meta
        context['total_evolucoes'] = context['evolucoes'].count()
        return context

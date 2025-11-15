from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, View
from django.urls import reverse
from django.db import transaction
from atendimentos.models import Atendimento
from usuarios.models import Profissional
from .models import Evolucao, SinalVital, Prescricao, SolicitacaoExame, ResultadoExame
from .forms import EvolucaoForm, SinalVitalForm, PrescricaoForm, ItemPrescricaoFormSet, SolicitacaoExameForm, ResultadoExameForm


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


class NovoSinalVitalView(LoginRequiredMixin, FormView):
    """View para adicionar novo registro de sinais vitais a um atendimento"""
    template_name = 'prontuario/novo_sinal_vital.html'
    form_class = SinalVitalForm

    def get_success_url(self):
        """Retorna para a timeline de sinais vitais do atendimento"""
        return reverse('sinais_vitais_atendimento', kwargs={'atendimento_id': self.kwargs['atendimento_id']})

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
        """Salva sinal vital vinculando atendimento e profissional automaticamente"""
        sinal_vital = form.save(commit=False)

        # Vincula atendimento
        sinal_vital.atendimento = get_object_or_404(Atendimento, pk=self.kwargs['atendimento_id'])

        # Vincula profissional logado
        try:
            sinal_vital.profissional = self.request.user.profissional
        except Profissional.DoesNotExist:
            messages.error(
                self.request,
                'Erro: Seu usuário não possui perfil de profissional vinculado.'
            )
            return redirect('dashboard')

        sinal_vital.save()

        # Verifica se há sinais alterados e exibe alertas
        alertas = sinal_vital.tem_sinais_alterados()
        if alertas:
            messages.warning(
                self.request,
                f'Sinais vitais registrados com alertas: {", ".join(alertas)}'
            )
        else:
            messages.success(
                self.request,
                'Sinais vitais registrados com sucesso!'
            )

        return super().form_valid(form)


class SinaisVitaisAtendimentoView(LoginRequiredMixin, DetailView):
    """View para listar timeline de sinais vitais de um atendimento"""
    model = Atendimento
    template_name = 'prontuario/sinais_vitais_atendimento.html'
    pk_url_kwarg = 'atendimento_id'
    context_object_name = 'atendimento'

    def get_queryset(self):
        """Otimiza query com prefetch de sinais vitais"""
        return Atendimento.objects.select_related(
            'paciente',
            'profissional_responsavel__user'
        ).prefetch_related(
            'sinais_vitais__profissional__user'
        )

    def get_context_data(self, **kwargs):
        """Adiciona sinais vitais ao contexto (ordem cronológica reversa)"""
        context = super().get_context_data(**kwargs)
        context['sinais_vitais'] = self.object.sinais_vitais.select_related(
            'profissional__user'
        ).all()  # Já ordenado por -data_hora no Model Meta
        context['total_sinais_vitais'] = context['sinais_vitais'].count()
        return context


class NovaPrescricaoView(LoginRequiredMixin, View):
    """View para criar nova prescrição médica (apenas perfil MEDICO)"""
    template_name = 'prontuario/nova_prescricao.html'

    def dispatch(self, request, *args, **kwargs):
        """Verifica se o usuário é médico antes de permitir acesso"""
        try:
            profissional = request.user.profissional
            if profissional.perfil != 'MEDICO':
                messages.error(
                    request,
                    'Apenas médicos podem criar prescrições médicas.'
                )
                return redirect('dashboard')
        except Profissional.DoesNotExist:
            messages.error(
                request,
                'Erro: Seu usuário não possui perfil de profissional vinculado.'
            )
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, atendimento_id):
        """Exibe formulário vazio de prescrição"""
        atendimento = get_object_or_404(
            Atendimento.objects.select_related('paciente'),
            pk=atendimento_id
        )

        form = PrescricaoForm()
        formset = ItemPrescricaoFormSet()

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'atendimento': atendimento,
        })

    def post(self, request, atendimento_id):
        """Processa formulário de prescrição com itens"""
        atendimento = get_object_or_404(
            Atendimento.objects.select_related('paciente'),
            pk=atendimento_id
        )

        form = PrescricaoForm(request.POST)
        formset = ItemPrescricaoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Salva prescrição
                    prescricao = form.save(commit=False)
                    prescricao.atendimento = atendimento
                    prescricao.profissional = request.user.profissional
                    prescricao.save()

                    # Salva itens da prescrição
                    formset.instance = prescricao
                    formset.save()

                    messages.success(
                        request,
                        f'Prescrição registrada com sucesso com {prescricao.total_itens()} medicamento(s)!'
                    )

                    return redirect('prescricoes_atendimento', atendimento_id=atendimento.id)

            except Exception as e:
                messages.error(
                    request,
                    f'Erro ao salvar prescrição: {str(e)}'
                )

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'atendimento': atendimento,
        })


class PrescricoesAtendimentoView(LoginRequiredMixin, DetailView):
    """View para listar prescrições de um atendimento"""
    model = Atendimento
    template_name = 'prontuario/prescricoes_atendimento.html'
    pk_url_kwarg = 'atendimento_id'
    context_object_name = 'atendimento'

    def get_queryset(self):
        """Otimiza query com prefetch de prescrições"""
        return Atendimento.objects.select_related(
            'paciente',
            'profissional_responsavel__user'
        ).prefetch_related(
            'prescricoes__profissional__user',
            'prescricoes__itens'
        )

    def get_context_data(self, **kwargs):
        """Adiciona prescrições ao contexto"""
        context = super().get_context_data(**kwargs)
        context['prescricoes'] = self.object.prescricoes.select_related(
            'profissional__user'
        ).prefetch_related('itens').all()
        context['total_prescricoes'] = context['prescricoes'].count()
        context['prescricoes_ativas'] = context['prescricoes'].filter(status='ATIVA').count()

        # Verifica se o usuário é médico para mostrar botão de nova prescrição
        try:
            context['e_medico'] = self.request.user.profissional.perfil == 'MEDICO'
        except:
            context['e_medico'] = False

        return context


class NovaSolicitacaoExameView(LoginRequiredMixin, FormView):
    """View para criar nova solicitação de exame (apenas perfil MEDICO)"""
    template_name = 'prontuario/nova_solicitacao_exame.html'
    form_class = SolicitacaoExameForm

    def dispatch(self, request, *args, **kwargs):
        """Verifica se o usuário é médico antes de permitir acesso"""
        try:
            profissional = request.user.profissional
            if profissional.perfil != 'MEDICO':
                messages.error(
                    request,
                    'Apenas médicos podem solicitar exames.'
                )
                return redirect('dashboard')
        except Profissional.DoesNotExist:
            messages.error(
                request,
                'Erro: Seu usuário não possui perfil de profissional vinculado.'
            )
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Retorna para a listagem de solicitações do atendimento"""
        return reverse('solicitacoes_exame_atendimento', kwargs={'atendimento_id': self.kwargs['atendimento_id']})

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
        """Salva solicitação vinculando atendimento e profissional automaticamente"""
        solicitacao = form.save(commit=False)

        # Vincula atendimento
        solicitacao.atendimento = get_object_or_404(Atendimento, pk=self.kwargs['atendimento_id'])

        # Vincula profissional logado
        solicitacao.profissional = self.request.user.profissional

        solicitacao.save()

        messages.success(
            self.request,
            f'Exame solicitado com sucesso: {solicitacao.nome_exame}'
        )

        return super().form_valid(form)


class SolicitacoesExameAtendimentoView(LoginRequiredMixin, DetailView):
    """View para listar solicitações de exames de um atendimento"""
    model = Atendimento
    template_name = 'prontuario/solicitacoes_exame_atendimento.html'
    pk_url_kwarg = 'atendimento_id'
    context_object_name = 'atendimento'

    def get_queryset(self):
        """Otimiza query com prefetch de solicitações"""
        return Atendimento.objects.select_related(
            'paciente',
            'profissional_responsavel__user'
        ).prefetch_related(
            'solicitacoes_exame__profissional__user',
            'solicitacoes_exame__resultado'
        )

    def get_context_data(self, **kwargs):
        """Adiciona solicitações ao contexto"""
        context = super().get_context_data(**kwargs)
        context['solicitacoes'] = self.object.solicitacoes_exame.select_related(
            'profissional__user'
        ).prefetch_related('resultado').all()
        context['total_solicitacoes'] = context['solicitacoes'].count()
        context['solicitacoes_pendentes'] = context['solicitacoes'].filter(
            status__in=['SOLICITADO', 'COLETADO']
        ).count()

        # Verifica se o usuário é médico para mostrar botão de nova solicitação
        try:
            context['e_medico'] = self.request.user.profissional.perfil == 'MEDICO'
        except:
            context['e_medico'] = False

        return context


class AdicionarResultadoExameView(LoginRequiredMixin, FormView):
    """View para adicionar resultado a uma solicitação de exame"""
    template_name = 'prontuario/adicionar_resultado_exame.html'
    form_class = ResultadoExameForm

    def get_success_url(self):
        """Retorna para a listagem de solicitações do atendimento"""
        solicitacao = get_object_or_404(SolicitacaoExame, pk=self.kwargs['solicitacao_id'])
        return reverse('solicitacoes_exame_atendimento', kwargs={'atendimento_id': solicitacao.atendimento.id})

    def get_context_data(self, **kwargs):
        """Adiciona solicitação e atendimento ao contexto"""
        context = super().get_context_data(**kwargs)
        solicitacao = get_object_or_404(
            SolicitacaoExame.objects.select_related(
                'atendimento__paciente',
                'profissional__user'
            ),
            pk=self.kwargs['solicitacao_id']
        )
        context['solicitacao'] = solicitacao
        context['atendimento'] = solicitacao.atendimento
        return context

    def form_valid(self, form):
        """Salva resultado e atualiza status da solicitação"""
        solicitacao = get_object_or_404(SolicitacaoExame, pk=self.kwargs['solicitacao_id'])

        # Verifica se já existe resultado
        if hasattr(solicitacao, 'resultado'):
            messages.error(
                self.request,
                'Esta solicitação já possui resultado registrado.'
            )
            return redirect('solicitacoes_exame_atendimento', atendimento_id=solicitacao.atendimento.id)

        resultado = form.save(commit=False)
        resultado.solicitacao = solicitacao
        resultado.save()

        # Atualiza status da solicitação
        solicitacao.status = 'RESULTADO_DISPONIVEL'
        solicitacao.save()

        messages.success(
            self.request,
            f'Resultado registrado com sucesso para: {solicitacao.nome_exame}'
        )

        return super().form_valid(form)


class CancelarExameView(LoginRequiredMixin, View):
    """View para cancelar uma solicitação de exame (apenas médico solicitante)"""

    def post(self, request, solicitacao_id):
        """Cancela a solicitação de exame"""
        solicitacao = get_object_or_404(
            SolicitacaoExame.objects.select_related('profissional', 'atendimento'),
            pk=solicitacao_id
        )

        # Verifica se o usuário é médico
        try:
            profissional = request.user.profissional
            if profissional.perfil != 'MEDICO':
                messages.error(request, 'Apenas médicos podem cancelar solicitações de exames.')
                return redirect('solicitacoes_exame_atendimento', atendimento_id=solicitacao.atendimento.id)
        except Profissional.DoesNotExist:
            messages.error(request, 'Erro: Seu usuário não possui perfil de profissional vinculado.')
            return redirect('dashboard')

        # Verifica se já foi cancelado
        if solicitacao.status == 'CANCELADO':
            messages.warning(request, 'Esta solicitação já está cancelada.')
            return redirect('solicitacoes_exame_atendimento', atendimento_id=solicitacao.atendimento.id)

        # Verifica se já tem resultado
        if hasattr(solicitacao, 'resultado'):
            messages.error(request, 'Não é possível cancelar uma solicitação que já possui resultado.')
            return redirect('solicitacoes_exame_atendimento', atendimento_id=solicitacao.atendimento.id)

        # Cancela solicitação
        solicitacao.status = 'CANCELADO'
        solicitacao.save()

        messages.success(request, f'Solicitação de exame cancelada: {solicitacao.nome_exame}')

        return redirect('solicitacoes_exame_atendimento', atendimento_id=solicitacao.atendimento.id)

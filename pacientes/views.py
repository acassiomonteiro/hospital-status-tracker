from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from .models import Paciente
from .forms import PacienteBuscaForm


class BuscarPacienteView(LoginRequiredMixin, ListView):
    """View para busca avançada de pacientes"""
    model = Paciente
    template_name = 'pacientes/buscar_paciente.html'
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        """Aplica filtros de busca no queryset"""
        queryset = Paciente.objects.all()
        form = PacienteBuscaForm(self.request.GET)

        if form.is_valid():
            cpf = form.cleaned_data.get('cpf')
            nome = form.cleaned_data.get('nome')
            data_nascimento = form.cleaned_data.get('data_nascimento')

            # Filtro por CPF (busca parcial)
            if cpf:
                queryset = queryset.filter(cpf__icontains=cpf)

            # Filtro por nome (case-insensitive)
            if nome:
                queryset = queryset.filter(nome__icontains=nome)

            # Filtro por data de nascimento (exata)
            if data_nascimento:
                queryset = queryset.filter(data_nascimento=data_nascimento)

        # Ordena por nome
        queryset = queryset.order_by('nome')

        return queryset

    def get_context_data(self, **kwargs):
        """Adiciona form e total de resultados ao contexto"""
        context = super().get_context_data(**kwargs)
        context['form'] = PacienteBuscaForm(self.request.GET)
        context['total_resultados'] = self.get_queryset().count()
        context['tem_filtros'] = bool(self.request.GET)
        return context

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """View customizada para login"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f'Bem-vindo(a), {self.request.user.get_full_name() or self.request.user.username}!')
        return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    """View customizada para logout"""
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Você saiu do sistema com sucesso.')
        return super().dispatch(request, *args, **kwargs)

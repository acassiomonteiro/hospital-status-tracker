"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('', include('atendimentos.urls')),
    path('', include('prontuario.urls')),
    path('', include('ia.urls'))
]

# Configuração para servir arquivos estáticos e media em desenvolvimento
# staticfiles_urlpatterns usa o sistema de finders do Django para localizar arquivos estáticos
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    # Servir arquivos de media (uploads)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

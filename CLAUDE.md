# Hospital Status Tracker - Sistema de Rastreamento de Pacientes

## Visão Geral

Sistema web MVP para rastreamento em tempo real do status de pacientes no pronto-socorro do Hospital Santa Helena Norte. Projeto acadêmico (PBL) focado em resolver fragmentação de informações clínicas.

---

## Stack Tecnológica

- **Backend**: Django 5.0.1 + Python 3.12
- **Frontend**: Django Templates + Tailwind CSS 3.x (via CDN)
- **Banco de Dados**: SQLite (dev) / PostgreSQL (produção futura)
- **Autenticação**: Django Auth nativo (User + Profissional)

---

## Estrutura de Arquivos

```
hospital-status-tracker/
├── manage.py
├── CLAUDE.md                    # Este arquivo
├── hospital/                    # Configuração Django
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URL raiz (inclui atendimento.urls)
│   └── wsgi.py
├── atendimento/                # App principal
│   ├── models.py               # Paciente, Atendimento, Profissional
│   ├── views.py                # CBVs: Dashboard, Novo, Atualizar
│   ├── urls.py                 # Rotas: /, /novo/, /atualizar/<id>/
│   ├── forms.py                # PacienteForm, AtendimentoForm
│   ├── admin.py                # Config admin Django
│   └── templates/
│       ├── atendimento/
│       │   ├── base.html       # Template base com Tailwind
│       │   ├── dashboard.html  # Lista de atendimentos
│       │   ├── novo_atendimento.html
│       │   └── atualizar_status.html
│       └── registration/
│           └── login.html      # (a ser criado)
└── db.sqlite3                  # Banco local
```

---

## Models Atuais

### Paciente

- `nome`: CharField (200 chars)
- `cpf`: CharField (11 chars, unique, validado com regex)
- `data_nascimento`: DateField
- `criado_em`: DateTimeField (auto)

### Atendimento

- `paciente`: ForeignKey → Paciente (PROTECT)
- `data_hora_entrada`: DateTimeField (auto)
- `queixa`: TextField
- `status`: CharField com 7 choices (default: TRIAGEM)
- `atualizado_em`: DateTimeField (auto)

**Status disponíveis:**
1. TRIAGEM
2. EM_ATENDIMENTO
3. AGUARDANDO_EXAME
4. EM_EXAME
5. AGUARDANDO_RESULTADO
6. ALTA
7. INTERNACAO

**Método útil:** `get_status_badge_class()` retorna classe Tailwind por status

---

## Padrões de Código

### Geral

- **Idioma**: Nomes de models, campos e variáveis em português
- **Style Guide**: PEP 8 (linhas até 100 chars)
- **Imports**: Ordem padrão Django (stdlib → django → terceiros → local)

### Models

- Sempre usar `verbose_name` em português
- ForeignKeys com `on_delete=models.PROTECT` (segurança de dados)
- `related_name` descritivo quando apropriado
- Método `__str__()` obrigatório

### Views

- **Preferir CBVs** (Class-Based Views): ListView, FormView, DetailView
- Usar `LoginRequiredMixin` para proteger views (a ser implementado)
- `select_related()` e `prefetch_related()` para otimizar queries
- Messages framework para feedback ao usuário

### Forms

- Validação no Form E no Model (dupla camada)
- `clean_<campo>()` para validações customizadas
- Labels em português

### Templates

- **Herança**: Todos herdam de `base.html`
- **Estilo**: Tailwind CSS inline (classes diretas no HTML)
- **Mobile-first**: Design responsivo prioritário
- **Acessibilidade**: Usar tags semânticas (header, nav, main, footer)

---

## Convenções Específicas

### Validação de CPF

```python
# No model: RegexValidator(regex=r'^\d{11}$')
# No form: clean_cpf() remove caracteres não numéricos
```

### Feedback ao Usuário

```python
from django.contrib import messages
messages.success(request, 'Atendimento criado com sucesso!')
```

### Queries Otimizadas

```python
# SEMPRE use select_related para ForeignKeys
atendimentos = Atendimento.objects.select_related('paciente')
```

---

## Comandos Rápidos

### Desenvolvimento

```bash
# Criar e aplicar migrations
python manage.py makemigrations && python manage.py migrate

# Rodar servidor
python manage.py runserver

# Shell interativo
python manage.py shell

# Criar superusuário
python manage.py createsuperuser
```

### Úteis

```bash
# Ver SQL de uma migration
python manage.py sqlmigrate atendimento 0001

# Verificar problemas
python manage.py check

# Limpar cache
python manage.py flush --noinput
```

---

## Regras para Novas Funcionalidades

### ✅ Sempre Fazer

- [ ] Criar migration após alterar models
- [ ] Testar no navegador antes de commitar
- [ ] Adicionar validações no model E no form
- [ ] Usar messages para feedback
- [ ] Manter consistência visual (Tailwind)
- [ ] Documentar mudanças complexas com comentários

### ❌ Nunca Fazer

- ❌ Quebrar funcionalidades existentes
- ❌ Remover migrations já aplicadas
- ❌ Usar JavaScript externo (manter simples)
- ❌ Adicionar dependências sem necessidade
- ❌ Hardcode de valores (usar constantes)
- ❌ Expor dados sensíveis no template

---

## Próximas Funcionalidades Planejadas

### FASE 1: Autenticação (PRÓXIMO) 🔴

- [ ] Model Profissional (OneToOne com User)
- [ ] LoginView e LogoutView
- [ ] Proteger views com LoginRequiredMixin
- [ ] Template de login
- [ ] Navbar com nome do usuário

### FASE 2: Dados Clínicos Expandidos

- [ ] Expandir Paciente (telefone, endereço, alergias)
- [ ] Model Evolucao (notas clínicas)
- [ ] Model SinalVital

### FASE 3: Prescrições e Exames

- [ ] Model Prescricao
- [ ] Model SolicitacaoExame
- [ ] Upload de laudos

### FASE 4: Prontuário Completo

- [ ] View de histórico consolidado
- [ ] Timeline de eventos
- [ ] Impressão de documentos

---

## Contexto Importante para IA

### Quando Modificar Código

1. **Leia o arquivo completo** antes de modificar
2. **Preserve funcionalidades existentes** - não remova código funcionando
3. **Siga os padrões estabelecidos** - mantenha consistência
4. **Teste mentalmente** - verifique se não vai quebrar nada

### Quando Criar Novas Features

1. **Comece pelos Models** - estrutura de dados primeiro
2. **Depois Forms** - validação e interface com usuário
3. **Depois Views** - lógica de negócio
4. **Por último Templates** - apresentação

### Segurança e Boas Práticas

- **Nunca** expor senhas ou tokens no código
- **Sempre** validar entrada do usuário
- **Sempre** usar CSRF protection (Django faz automaticamente)
- **Sempre** escapar output no template (Django faz automaticamente)

---

## Links Úteis

- Django Docs: https://docs.djangoproject.com/en/5.0/
- Tailwind CSS: https://tailwindcss.com/docs
- PEP 8: https://pep8.org/

---

## Notas do Projeto

- **Objetivo acadêmico**: PBL do 5º período - Programação para Web
- **Professor**: Esp. Guilherme Ferreira dos Reis
- **Prazo final**: 27 de novembro de 2025
- **Repositório**: https://github.com/acassiomonteiro/hospital-status-tracker

# Hospital Status Tracker - Sistema de Rastreamento de Pacientes

## Visão Geral
Sistema web MVP para rastreamento em tempo real do status de pacientes no pronto-socorro do Hospital Santa Helena Norte. Projeto acadêmico (PBL) focado em resolver fragmentação de informações clínicas.

---

## Stack Tecnológica
- **Backend**: Django 5.2.7 + Python 3.11
- **Frontend**: Django Templates + Tailwind CSS 3.x (via CDN)
- **Banco de Dados**: PostgreSQL (com Docker Compose)
- **Autenticação**: Django Auth nativo (User + Profissional)
- **Deploy**: Docker + Docker Compose

---

## Estrutura de Arquivos
```
hospital-status-tracker/
├── manage.py
├── CLAUDE.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Container da aplicação
├── docker-compose.yml           # Orquestração de serviços
├── entrypoint.sh                # Script de inicialização (migrations automáticas)
├── core/                        # Configuração Django
│   ├── settings.py             # Configurações principais (PostgreSQL)
│   ├── urls.py                 # URL raiz (inclui atendimento.urls)
│   ├── wsgi.py
│   └── asgi.py
├── atendimento/                # App principal
│   ├── models.py               # Paciente, Atendimento, Profissional
│   ├── views.py                # CBVs: Dashboard, Novo, Atualizar, Login, Logout
│   ├── urls.py                 # Rotas: /, /novo/, /atualizar/<id>/, /login/, /logout/
│   ├── forms.py                # PacienteForm, AtendimentoForm
│   ├── admin.py                # Config admin Django
│   └── templates/
│       ├── atendimento/
│       │   ├── base.html       # Template base com Tailwind + Navbar
│       │   ├── dashboard.html  # Lista de atendimentos
│       │   ├── novo_atendimento.html
│       │   └── atualizar_status.html
│       └── registration/
│           └── login.html      # Template de login
└── staticfiles/                # Arquivos estáticos coletados
```

---

## Models Atuais

### Paciente ✅ Expandido (Prontuário Completo)

**Dados Básicos (obrigatórios):**
- `nome`: CharField (200 chars)
- `cpf`: CharField (11 chars, unique, validado com regex)
- `data_nascimento`: DateField
- `criado_em`: DateTimeField (auto)
- `atualizado_em`: DateTimeField (auto)

**Dados Pessoais (opcionais):**
- `sexo`: CharField (choices: M, F, O)
- `nome_mae`: CharField (200 chars)
- `telefone`: CharField (10-11 dígitos, validado)
- `email`: EmailField

**Documentos (opcionais):**
- `cartao_sus`: CharField (15 dígitos, validado)
- `rg`: CharField (20 chars)

**Endereço (opcionais):**
- `cep`: CharField (8 dígitos, validado)
- `rua`: CharField (200 chars)
- `numero`: CharField (10 chars)
- `bairro`: CharField (100 chars)
- `cidade`: CharField (100 chars)
- `uf`: CharField (2 chars, validado para maiúsculas)

**Dados Clínicos (opcionais):**
- `tipo_sanguineo`: CharField (choices: A+, A-, B+, B-, AB+, AB-, O+, O-)
- `alergias`: TextField
- `observacoes_clinicas`: TextField

**Métodos:**
- `get_endereco_completo()`: Retorna endereço formatado

### Profissional ✅ Implementado
- `user`: OneToOneField → User (CASCADE)
- `perfil`: CharField (choices: MEDICO, ENFERMEIRO, ADMINISTRATIVO)
- `registro_profissional`: CharField (50 chars, opcional - CRM, COREN, etc.)
- `criado_em`: DateTimeField (auto)

**Perfis disponíveis:**
1. MEDICO
2. ENFERMEIRO
3. ADMINISTRATIVO

### Atendimento
- `paciente`: ForeignKey → Paciente (PROTECT)
- `profissional_responsavel`: ForeignKey → Profissional (PROTECT, opcional)
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

**Métodos:**
- `get_status_badge_class()`: Retorna classe Tailwind por status

### Evolucao ✅ Implementado
- `atendimento`: ForeignKey → Atendimento (PROTECT)
- `profissional`: ForeignKey → Profissional (PROTECT)
- `tipo`: CharField (choices: ANAMNESE, EVOLUCAO_MEDICA, EVOLUCAO_ENFERMAGEM, EXAME_FISICO)
- `descricao`: TextField
- `data_hora`: DateTimeField (auto_now_add)

**Tipos de Evolução disponíveis:**
1. ANAMNESE
2. EVOLUCAO_MEDICA
3. EVOLUCAO_ENFERMAGEM
4. EXAME_FISICO

**Métodos:**
- `get_tipo_badge_class()`: Retorna classe Tailwind por tipo de evolução

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
- ✅ **Todas as views protegidas com `LoginRequiredMixin`**
- `select_related()` e `prefetch_related()` para otimizar queries
- Messages framework para feedback ao usuário
- **Views de autenticação**: `CustomLoginView`, `CustomLogoutView`
- **Lógica de negócio**: `get_or_create` para evitar pacientes duplicados

### Forms
- Validação no Form E no Model (dupla camada)
- `clean_<campo>()` para validações customizadas
- Labels em português
- **PacienteForm expandido**: Todos os campos do prontuário
- **Validações automáticas**: Remove caracteres não numéricos (CPF, telefone, CEP, SUS)
- **Widgets customizados**: Classes Tailwind CSS aplicadas

### Templates
- **Herança**: Todos herdam de `base.html`
- **Estilo**: Tailwind CSS inline (classes diretas no HTML)
- **Mobile-first**: Design responsivo prioritário
- **Acessibilidade**: Usar tags semânticas (header, nav, main, footer)

---

## Convenções Específicas

### Validações Implementadas
```python
# CPF: RegexValidator(regex=r'^\d{11}$') + clean_cpf() remove não numéricos
# Telefone: RegexValidator(regex=r'^\d{10,11}$') + clean_telefone()
# CEP: RegexValidator(regex=r'^\d{8}$') + clean_cep()
# Cartão SUS: RegexValidator(regex=r'^\d{15}$') + clean_cartao_sus()
# UF: RegexValidator(regex=r'^[A-Z]{2}$') + clean_uf() converte para maiúsculas
```

### Feedback ao Usuário
```python
from django.contrib import messages
messages.success(request, 'Atendimento criado com sucesso!')
```

### Queries Otimizadas
```python
# SEMPRE use select_related para ForeignKeys
atendimentos = Atendimento.objects.select_related(
    'paciente', 
    'profissional_responsavel__user'
).all()
```

### Evitar Duplicação de Pacientes
```python
# Usar get_or_create para evitar pacientes duplicados pelo CPF
paciente, created = Paciente.objects.get_or_create(
    cpf=cpf,
    defaults={'nome': nome, 'data_nascimento': data_nascimento}
)
```

---

## Ambiente Docker

O projeto é **100% dockerizado** com migrations automáticas via `entrypoint.sh`.

### Comandos Docker
```bash
# Iniciar serviços (web + postgres)
docker-compose up

# Rebuild após mudanças
docker-compose down
docker-compose up --build

# Ver logs em tempo real
docker-compose logs -f web

# Acessar shell Django no container
docker-compose exec web python manage.py shell

# Criar superusuário (se necessário)
docker-compose exec web python manage.py createsuperuser

# Acessar banco PostgreSQL
docker-compose exec db psql -U hospital_admin -d hospital_db
```

**IMPORTANTE:** 
- Migrations são aplicadas **AUTOMATICAMENTE** pelo `entrypoint.sh` ao subir o container
- Após modificar models, basta fazer: `docker-compose down && docker-compose up --build`
- **NÃO** é necessário rodar `makemigrations` ou `migrate` manualmente

---

## Regras para Novas Funcionalidades

### ✅ Sempre Fazer
- [ ] Criar migration após alterar models
- [ ] Testar no navegador antes de commitar
- [ ] Adicionar validações no model E no form
- [ ] Usar messages para feedback
- [ ] Manter consistência visual (Tailwind)
- [ ] Documentar mudanças complexas com comentários
- [ ] Proteger views com LoginRequiredMixin
- [ ] Usar select_related/prefetch_related para otimizar queries
- [ ] Testar com Docker antes de fazer commit

### ❌ Nunca Fazer
- ❌ Quebrar funcionalidades existentes
- ❌ Remover migrations já aplicadas
- ❌ Usar JavaScript externo (manter simples)
- ❌ Adicionar dependências sem necessidade
- ❌ Hardcode de valores (usar constantes)
- ❌ Expor dados sensíveis no template
- ❌ Commitar variáveis de ambiente (.env) no Git
- ❌ Usar SQLite em produção (usar PostgreSQL)

---

## Roadmap de Desenvolvimento

### ✅ FASE 1: AUTENTICAÇÃO (COMPLETA)
- [x] Model Profissional (OneToOne com User)
- [x] 3 perfis de acesso: Médico, Enfermeiro, Administrativo
- [x] LoginView e LogoutView customizados
- [x] Todas as views protegidas com LoginRequiredMixin
- [x] Template de login responsivo
- [x] Navbar com nome do usuário e perfil
- [x] Vinculação de profissional aos atendimentos

**Problema da PBL resolvido:**
> "Credenciais genéricas compartilhadas por turno, inviabilizando rastreabilidade"

✅ Cada profissional tem login único e ações são rastreáveis.

---

### ✅ FASE 2: DADOS DO PACIENTE (COMPLETA)
- [x] Expandir Paciente com dados pessoais (telefone, email, sexo, nome_mae)
- [x] Adicionar documentação (Cartão SUS, RG)
- [x] Adicionar endereço completo (CEP, rua, número, bairro, cidade, UF)
- [x] Adicionar dados clínicos (tipo sanguíneo, alergias, observações)
- [x] Todos os novos campos opcionais (backward compatibility)
- [x] Validações em todos os campos
- [x] Formulário completo com widgets customizados
- [x] Docker e PostgreSQL configurados

**Problema da PBL resolvido:**
> "Cadastros com grafias distintas, variações de CPF, reaproveitamento"

✅ Identificação mais precisa com múltiplos dados + validações rigorosas.

---

### ✅ FASE 3: EVOLUÇÃO CLÍNICA (COMPLETA)

**Por que é crítica:** É o **coração do prontuário eletrônico**. Sem evoluções clínicas, o sistema é apenas "cadastro + status", não um prontuário real.

- [x] Model Evolucao vinculado a Atendimento e Profissional
- [x] 4 tipos de evolução: ANAMNESE, EVOLUCAO_MEDICA, EVOLUCAO_ENFERMAGEM, EXAME_FISICO
- [x] Campo descricao (TextField) para texto da evolução
- [x] Data/hora automática (auto_now_add)
- [x] Form de registro rápido (tipo + descricao)
- [x] View para adicionar evolução
- [x] View para listar evoluções (timeline cronológica)
- [x] Template com cards coloridos por tipo
- [x] Botão "Ver Evoluções" no dashboard

**Problema da PBL que resolve:**
> "Prontuário existe como combinação de papel, telas do legado e arquivos externos"

✅ Tudo num único lugar digital, com timeline completa do atendimento.

---

### 🟡 FASE 4: SINAIS VITAIS (PRÓXIMA - CRÍTICA!)

- [ ] Model SinalVital vinculado a Atendimento e Profissional
- [ ] Campos: pressao_arterial (sistólica/diastólica), frequencia_cardiaca, frequencia_respiratoria, temperatura, saturacao_o2, glicemia
- [ ] Form rápido para enfermagem
- [ ] Listagem por atendimento
- [ ] Gráficos de evolução temporal (opcional)

**Problema da PBL que resolve:**
> "Quadros brancos físicos e planilhas produzem instantâneos que se desatualizam"

✅ Sinais vitais digitalizados, timestamped e persistentes.

---

### 🟢 FASE 5: PRESCRIÇÕES MÉDICAS

- [ ] Model Prescricao (atendimento, profissional, data, validade)
- [ ] Model ItemPrescricao (medicamento, dose, via, frequência, duração)
- [ ] Form de prescrição
- [ ] Listagem de prescrições ativas
- [ ] Verificação de alergias ao prescrever

**Problema da PBL que resolve:**
> "Políticas de acesso não refletem necessidade de segregação por perfil"

✅ Só médico prescreve, registro auditável, alergias visíveis.

---

### 🟢 FASE 6: EXAMES (DESEJÁVEL)

- [ ] Model SolicitacaoExame (tipo, nome, justificativa, status)
- [ ] Model ResultadoExame (resultado, arquivo_laudo, data)
- [ ] Upload de laudos (FileField)
- [ ] Rastreamento de solicitações
- [ ] Status: SOLICITADO, COLETADO, CONCLUIDO

**Problema da PBL que resolve:**
> "Resultados disponibilizados em portais de terceiros, notificações por email genérico"

✅ Centraliza solicitações, mesmo que resultados venham de fora há vínculo claro.

---

### 🟢 FASE 7: PRONTUÁRIO COMPLETO (FECHAMENTO)

- [ ] View consolidada mostrando TUDO do paciente
- [ ] Timeline cronológica completa
- [ ] Dashboard integrado por atendimento
- [ ] Impressão de documentos (PDF futuro)
- [ ] Filtros e buscas avançadas

**Problema da PBL que resolve:**
> "Ecossistema informacional fragmentado"

✅ Ecossistema UNIFICADO em uma única view consolidada!

---

## Estado Atual do Projeto

### ✅ Funcionalidades Implementadas

**FASE 1 - Autenticação:** ✅ COMPLETA
- Sistema de login/logout funcional
- 3 perfis de usuário implementados
- Todas as views protegidas
- Navbar com informações do usuário

**FASE 2 - Dados do Paciente:** ✅ COMPLETA
- Prontuário completo com 20+ campos
- Validações robustas em todos os campos
- Formulário responsivo e organizado
- Infraestrutura Docker + PostgreSQL

**FASE 3 - Evolução Clínica:** ✅ COMPLETA
- Registro de evoluções clínicas por profissionais.
- Timeline cronológica completa por atendimento.
- Distinção visual para tipos de evolução (Médica, Enfermagem, etc.).

### 🎯 Próximo Passo

**FASE 4 - Sinais Vitais** (CRÍTICA - Prioridade Máxima)

O próximo passo é permitir o registro de sinais vitais (pressão, temperatura, etc.), digitalizando outra parte crucial do atendimento e permitindo o acompanhamento da evolução do paciente de forma estruturada.

---

## Contexto Importante para IA

### Quando Modificar Código
1. **Leia o arquivo completo** antes de modificar
2. **Preserve funcionalidades existentes** - não remova código funcionando
3. **Siga os padrões estabelecidos** - mantenha consistência
4. **Teste mentalmente** - verifique se não vai quebrar nada
5. **Mantenha validações** - não remova validações de campos

### Quando Criar Novas Features
1. **Comece pelos Models** - estrutura de dados primeiro
2. **Depois Forms** - validação e interface com usuário
3. **Depois Views** - lógica de negócio (com LoginRequiredMixin)
4. **Por último Templates** - apresentação

### Segurança e Boas Práticas
- **Nunca** expor senhas ou tokens no código
- **Sempre** validar entrada do usuário (model + form)
- **Sempre** usar CSRF protection (Django faz automaticamente)
- **Sempre** escapar output no template (Django faz automaticamente)
- **Sempre** proteger views com LoginRequiredMixin
- **Sempre** usar variáveis de ambiente para configurações sensíveis

### Docker e Ambiente
- **Migrations automáticas:** `entrypoint.sh` cuida disso
- **Não rodar comandos manuais:** Docker gerencia tudo
- **Rebuild após mudanças:** `docker-compose down && docker-compose up --build`
- **PostgreSQL em produção:** Nunca usar SQLite

---

## Links Úteis
- Django Docs: https://docs.djangoproject.com/en/5.2/
- Tailwind CSS: https://tailwindcss.com/docs
- PEP 8: https://pep8.org/
- Docker Docs: https://docs.docker.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/

---

## Notas do Projeto
- **Objetivo acadêmico**: PBL do 5º período - Programação para Web
- **Professor**: Esp. Guilherme Ferreira dos Reis
- **Prazo final**: 27 de novembro de 2025
- **Repositório**: https://github.com/acassiomonteiro/hospital-status-tracker
- **Aluno**: Acássio Monteiro
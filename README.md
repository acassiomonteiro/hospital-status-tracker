# 🏥 Hospital Status Tracker

Sistema de Rastreamento de Status de Pacientes no Pronto-Socorro

## 📋 Funcionalidades Implementadas (MVP)

- ✅ Cadastro de pacientes com validação de CPF
- ✅ Registro de atendimento vinculado ao paciente
- ✅ Sistema de 7 status: Triagem, Em Atendimento, Aguardando Exame, Em Exame, Aguardando Resultado, Alta, Internação
- ✅ Dashboard visual listando todos os atendimentos
- ✅ Atualização de status com feedback visual (cores)
- ✅ Interface responsiva com Tailwind CSS
- ✅ Django Admin configurado

## 🚀 Como Rodar
```bash
# Criar e a Venv
python -m venv venv
# Ativar a Venv
venv\Scripts\activate

# Se tiver no PowerShell, lembrar da policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Instalar dependências
pip install Django==5.0.1

# Criar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

## 🌐 Acessar

- Dashboard: http://localhost:8000/
- Cadastro: http://localhost:8000/novo/
- Admin: http://localhost:8000/admin/

## 🛠️ Tecnologias

- Python 3.12
- Django 5.0.1
- SQLite
- Tailwind CSS (CDN)

## 📅 Próximas Entregas

- [ ] Sistema de autenticação com 3 perfis
- [ ] Histórico de transições de status
- [ ] Logs de auditoria completos
- [ ] Dashboard com filtros e estatísticas
- [ ] Relatórios gerenciais

## 👨‍💻 Autor

Acássio Monteiro - UNDB - 5º Período - Sistemas de Informação

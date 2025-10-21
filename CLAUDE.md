# Hospital Status Tracker - Sistema de Rastreamento de Pacientes

## Contexto do Projeto
Sistema web para rastreamento em tempo real do status de pacientes no pronto-socorro do Hospital Santa Helena Norte.

## Stack Tecnológica
- Backend: Django 5.x
- Frontend: Django Templates + Tailwind CSS (via CDN)
- Banco de Dados: SQLite (desenvolvimento)
- Autenticação: Django Auth nativo

## Funcionalidades Principais
1. Cadastro único de pacientes (nome, CPF, data nascimento)
2. Registro de atendimento no PS
3. Atualização de status (7 estados: Triagem, Em Atendimento, Aguardando Exame, Em Exame, Aguardando Resultado, Alta, Internação)
4. Dashboard visual listando todos os atendimentos
5. Histórico de transições com logs de auditoria
6. Sistema de autenticação com 3 perfis: Médico, Enfermagem, Administrativo

## Estrutura do Projeto
```
hospital-status-tracker/
├── manage.py
├── hospital/              # Projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── atendimento/          # App principal
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    └── templates/
```

## Padrões de Código
- Use nomes descritivos em português para models e campos
- Siga PEP 8
- Use Class-Based Views quando apropriado
- Sempre adicione validações no model e no form

## Comandos Úteis
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

## Notas Importantes
- Validar CPF no cadastro de pacientes
- Todo status_change deve gerar entrada no log de auditoria
- Templates devem ser responsivos (mobile-first)
- Usar Tailwind CSS via CDN (sem build)
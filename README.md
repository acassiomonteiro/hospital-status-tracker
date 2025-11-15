# 🏥 Hospital Status Tracker

Sistema de Rastreamento de Status de Pacientes no Pronto-Socorro. Este é um projeto acadêmico (PBL) que visa criar um MVP para resolver a fragmentação de informações clínicas em tempo real.

## 🏗️ Arquitetura Modular

O projeto segue uma **arquitetura modular** dividida em 4 apps Django especializados:

- **`pacientes`**: Gerencia dados dos pacientes (prontuário eletrônico)
- **`usuarios`**: Gerencia profissionais e sistema de autenticação
- **`atendimentos`**: Gerencia o fluxo de atendimentos no pronto-socorro
- **`prontuario`**: Gerencia evoluções clínicas e registros médicos
- **`ia`**: Centraliza e gerencia toda a lógica e integração de inteligência artificial na aplicação

Esta separação proporciona **maior organização, escalabilidade e clareza** no desenvolvimento.

## ✅ Funcionalidades Implementadas

O projeto já conta com um conjunto robusto de funcionalidades divididas em três fases principais:

**FASE 1: Autenticação e Perfis** ✅
- Sistema de login e logout seguro com perfis de usuário (Médico, Enfermeiro, Administrativo).
- Proteção de todas as rotas, garantindo que apenas usuários autenticados acessem o sistema.
- Rastreabilidade de ações, vinculando cada atendimento ao profissional responsável.

**FASE 2: Prontuário Eletrônico do Paciente** ✅
- Cadastro de paciente expandido para um prontuário completo, com dados pessoais, documentos, endereço e informações clínicas.
- Validações robustas em campos como CPF, Cartão SUS, CEP e telefone para garantir a integridade dos dados.
- Dashboard principal que exibe todos os pacientes em atendimento e seus status atuais.
- Funcionalidade para atualizar o status do paciente (ex: de "Triagem" para "Em Atendimento").

**FASE 3: Evolução Clínica** ✅
- Registro de evoluções clínicas por profissionais (Anamnese, Evolução Médica, Evolução de Enfermagem, Exame Físico).
- Timeline cronológica completa por atendimento.
- Distinção visual para diferentes tipos de evolução.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11+ e Django 5.2+
- **Banco de Dados**: PostgreSQL
- **Frontend**: Templates Django com Tailwind CSS (via CDN)
- **Ambiente de Desenvolvimento**: Docker e Docker Compose

## 🚀 Como Executar o Projeto (Recomendado: Docker)

O projeto é 100% containerizado para simplificar a configuração e a execução.

1.  **Iniciar os Serviços**:
    Com Docker e Docker Compose instalados, execute o comando na raiz do projeto:
    ```bash
    docker-compose up --build
    ```
    Este comando irá construir as imagens, iniciar o container da aplicação e o do banco de dados.

2.  **Acessar o Sistema**:
    A aplicação estará disponível em `http://localhost:8000`.

**Observações Importantes**:
- As migrações do banco de dados são aplicadas **automaticamente** toda vez que o container é iniciado.
- O primeiro acesso pode levar um minuto extra enquanto o banco de dados é preparado.

### Comandos Úteis do Docker

```bash
# Criar um superusuário para acessar o Admin
docker-compose exec web python manage.py createsuperuser

# Acessar o shell do Django dentro do container
docker-compose exec web python manage.py shell

# Visualizar os logs da aplicação em tempo real
docker-compose logs -f web
```

<details>
  <summary>Alternativa: Execução Local (sem Docker)</summary>

  Se preferir rodar localmente, siga os passos abaixo:

  1.  **Ambiente Virtual**:
      ```bash
      python -m venv venv
      # Windows
      .\venv\Scripts\Activate.ps1
      # Linux/macOS
      source venv/bin/activate
      ```
  2.  **Dependências**:
      ```bash
      pip install -r requirements.txt
      ```
  3.  **Banco de Dados**:
      Certifique-se de ter um servidor PostgreSQL rodando localmente e configure as variáveis de ambiente (ou o `settings.py`) com suas credenciais.
  4.  **Executar Migrations**:
      ```bash
      python manage.py migrate
      ```
  5.  **Iniciar Servidor**:
      ```bash
      python manage.py runserver
      ```
</details>

## 🎯 Status e Próximos Passos

Atualmente, as fases de **Autenticação**, **Prontuário do Paciente** e **Evolução Clínica** estão completas.

O próximo foco crítico do projeto é a **FASE 4: Sinais Vitais**. Esta fase permitirá o registro estruturado de sinais vitais (pressão arterial, temperatura, frequência cardíaca, etc.), digitalizando outra parte crucial do atendimento e permitindo o acompanhamento da evolução do paciente de forma estruturada.

## 👨‍💻 Autor

Acássio Monteiro - UNDB - 5º Período - Sistemas de Informação

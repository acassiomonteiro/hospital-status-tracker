# Módulo de IA - Hospital Status Tracker

Este módulo contém ferramentas de Inteligência Artificial integradas com LangChain para consulta e análise de prontuários eletrônicos.

## 📋 Visão Geral

O módulo `ia` fornece tools LangChain que podem ser usadas por agentes de IA (LLMs) para:
- Buscar prontuários completos de pacientes
- Consultar histórico de atendimentos
- Acessar evoluções clínicas
- Realizar buscas por nome ou CPF

## 🗂️ Estrutura

```
ia/
├── README.md                    # Este arquivo
├── apps.py                      # Configuração do app Django
├── models.py                    # Models (futuro)
├── views.py                     # Views (futuro)
├── urls.py                      # URLs (futuro)
├── admin.py                     # Admin (futuro)
└── services/                    # Serviços de IA
    ├── __init__.py             # Exportações principais
    ├── tools.py                # Tools LangChain
    ├── agent.py                # Configuração do agente (futuro)
    ├── prompts.py              # Prompts do sistema (futuro)
    ├── runner.py               # Executor de agentes (futuro)
    ├── example_usage.py        # Exemplos práticos
    ├── test_tools.py           # Testes unitários
    └── TOOLS_USAGE.md          # Documentação completa
```

## 🚀 Quick Start

### Instalação

As dependências já estão incluídas no `requirements.txt`:
- `langchain-core==1.0.4`
- `langchain-openai==1.0.2`
- `openai==2.7.1`

### Uso Básico

```python
from ia.services import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
)

# Buscar prontuário por ID
prontuario = get_patient_record_by_id.invoke({'paciente_id': 1})
print(f"Paciente: {prontuario['nome']}")

# Buscar por CPF
prontuario = get_patient_record_by_cpf.invoke({'cpf': '12345678901'})

# Buscar pacientes por nome
resultados = search_patients.invoke({'nome': 'João'})
print(f"Encontrados: {resultados['total']} pacientes")

# Buscar evoluções de um atendimento
evolucoes = get_evolutions_for_attendance(atendimento_id=5)
```

## 🛠️ Tools Disponíveis

### 1. get_patient_record_by_id

Busca o prontuário completo de um paciente pelo ID.

**Parâmetros:**
- `paciente_id` (int): ID do paciente
- `include_attendance_history` (bool): Incluir histórico de atendimentos

**Retorna:** Dicionário com todos os dados do prontuário

---

### 2. get_patient_record_by_cpf

Busca o prontuário completo de um paciente pelo CPF.

**Parâmetros:**
- `cpf` (str): CPF do paciente (aceita formatação)
- `include_attendance_history` (bool): Incluir histórico de atendimentos

**Retorna:** Dicionário com todos os dados do prontuário

---

### 3. search_patients

Busca pacientes por nome ou CPF (busca parcial).

**Parâmetros:**
- `nome` (str, opcional): Nome ou parte do nome
- `cpf` (str, opcional): CPF ou parte do CPF
- `limit` (int): Máximo de resultados (padrão: 10)

**Retorna:** Lista de pacientes encontrados

---

### 4. get_evolutions_for_attendance

Busca todas as evoluções clínicas de um atendimento.

**Parâmetros:**
- `atendimento_id` (int): ID do atendimento

**Retorna:** Lista de evoluções com detalhes

---

## 🤖 Integração com LangChain Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from ia.services import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
)

# Configurar LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Lista de tools
tools = [
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
]

# Criar prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente médico especializado em consultar
    prontuários eletrônicos do Hospital Santa Helena Norte."""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Criar agente
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Executar consultas em linguagem natural
response = agent_executor.invoke({
    "input": "Busque o paciente João Silva e me diga suas alergias"
})
print(response["output"])
```

## 📊 Exemplos de Consultas

O agente LangChain pode responder perguntas como:

1. **"Busque o prontuário do paciente com CPF 12345678901"**
2. **"Quais são as alergias do paciente João Silva?"**
3. **"Mostre o histórico completo de atendimentos do paciente ID 5"**
4. **"Liste as evoluções clínicas do atendimento 10"**
5. **"Quantos atendimentos o paciente Maria teve?"**

## 🧪 Testes

Execute os testes com:

```bash
# Todos os testes
python manage.py test ia.services.test_tools

# Teste específico
python manage.py test ia.services.test_tools.PatientToolsTestCase.test_get_patient_record_by_id_basic

# Com verbose
python manage.py test ia.services.test_tools -v 2
```

## 📖 Documentação Completa

Para documentação detalhada, consulte:
- `ia/services/TOOLS_USAGE.md` - Documentação completa das tools
- `ia/services/example_usage.py` - Exemplos práticos executáveis
- `ia/services/test_tools.py` - Testes unitários

## 🔒 Segurança

As tools implementam as seguintes práticas de segurança:

1. **Validação de entrada**: Todos os parâmetros são validados
2. **Tratamento de erros**: Exceções são capturadas e retornadas estruturadamente
3. **Otimização de queries**: Uso de `select_related()` para evitar N+1
4. **Limitação de resultados**: Máximo de 50 resultados por busca
5. **Privacidade**: Nunca expõe senhas ou dados sensíveis

## 🚧 Roadmap

### Próximas Funcionalidades

1. **Fase 4 - Sinais Vitais**
   - Tool para buscar sinais vitais de um paciente
   - Tool para registrar novos sinais vitais
   - Análise de tendências (gráficos)

2. **Fase 5 - Prescrições**
   - Tool para buscar prescrições ativas
   - Tool para criar prescrições
   - Verificação automática de alergias

3. **Fase 6 - Exames**
   - Tool para buscar solicitações de exames
   - Tool para registrar resultados
   - Upload de laudos

4. **Fase 7 - Relatórios**
   - Tool para gerar relatórios consolidados
   - Análise estatística de atendimentos
   - Exportação em PDF

### Melhorias Técnicas

- [ ] Cache de resultados para queries frequentes
- [ ] Suporte a streaming de respostas
- [ ] Logs estruturados (logging)
- [ ] Métricas de performance
- [ ] Rate limiting para APIs externas
- [ ] Suporte a múltiplos idiomas

## 🤝 Contribuindo

Para adicionar novas tools:

1. Crie a função no arquivo `ia/services/tools.py`
2. Use o decorator `@tool` do LangChain
3. Documente os parâmetros e retorno
4. Adicione testes em `test_tools.py`
5. Exporte no `__init__.py`
6. Atualize a documentação

Exemplo:

```python
@tool
def minha_nova_tool(parametro: str) -> dict:
    """
    Descrição da tool.

    Args:
        parametro: Descrição do parâmetro

    Returns:
        Descrição do retorno
    """
    try:
        # Implementação
        return {'resultado': 'sucesso'}
    except Exception as e:
        return {'error': str(e)}
```

## 📝 Licença

Este projeto é parte do trabalho acadêmico do Hospital Status Tracker.

## 👥 Autores

- **Acássio Monteiro** - Desenvolvimento inicial
- **Esp. Guilherme Ferreira dos Reis** - Professor orientador

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `TOOLS_USAGE.md`
2. Veja os exemplos em `example_usage.py`
3. Execute os testes para validar o ambiente
4. Consulte o arquivo principal `CLAUDE.md` do projeto

---

**Última atualização:** Novembro 2025

# Tools LangChain - Hospital Status Tracker

Este documento descreve as tools disponíveis para integração com LangChain no sistema de rastreamento de pacientes.

## Tools Disponíveis

### 1. get_patient_record_by_id

Busca o prontuário completo de um paciente pelo ID.

**Parâmetros:**
- `paciente_id` (int): ID do paciente
- `include_attendance_history` (bool, opcional): Se True, inclui histórico completo de atendimentos e evoluções (default: False)

**Retorno:**
Dicionário completo com todos os dados do prontuário:
- Dados pessoais (nome, CPF, data de nascimento, sexo, etc.)
- Documentos (RG, Cartão SUS)
- Endereço completo
- Dados clínicos (tipo sanguíneo, alergias, observações)
- Histórico de atendimentos (se solicitado)

**Exemplo de uso:**

```python
from ia.services.tools import get_patient_record_by_id

# Buscar apenas dados cadastrais
prontuario = get_patient_record_by_id.invoke({'paciente_id': 1})

# Buscar com histórico completo
prontuario_completo = get_patient_record_by_id.invoke({
    'paciente_id': 1,
    'include_attendance_history': True
})

print(f"Paciente: {prontuario['nome']}")
print(f"CPF: {prontuario['cpf']}")
print(f"Tipo Sanguíneo: {prontuario['dados_clinicos']['tipo_sanguineo']}")

if 'historico_atendimentos' in prontuario_completo:
    print(f"Total de atendimentos: {prontuario_completo['total_atendimentos']}")
```

---

### 2. get_patient_record_by_cpf

Busca o prontuário completo de um paciente pelo CPF.

**Parâmetros:**
- `cpf` (str): CPF do paciente (11 dígitos, aceita formatação)
- `include_attendance_history` (bool, opcional): Se True, inclui histórico completo (default: False)

**Retorno:**
Mesmo formato do `get_patient_record_by_id`

**Exemplo de uso:**

```python
from ia.services.tools import get_patient_record_by_cpf

# Aceita CPF com ou sem formatação
prontuario = get_patient_record_by_cpf.invoke({'cpf': '12345678901'})
# ou
prontuario = get_patient_record_by_cpf.invoke({'cpf': '123.456.789-01'})

# Com histórico completo
prontuario_completo = get_patient_record_by_cpf.invoke({
    'cpf': '12345678901',
    'include_attendance_history': True
})
```

---

### 3. search_patients

Busca pacientes por nome ou CPF (busca parcial).

**Parâmetros:**
- `nome` (str, opcional): Nome ou parte do nome do paciente
- `cpf` (str, opcional): CPF ou parte do CPF do paciente
- `limit` (int, opcional): Número máximo de resultados (default: 10, máximo: 50)

**Retorno:**
Dicionário com:
- `total`: Total de pacientes encontrados
- `exibindo`: Número de pacientes retornados
- `pacientes`: Lista com dados básicos de cada paciente

**Exemplo de uso:**

```python
from ia.services.tools import search_patients

# Buscar por nome
resultados = search_patients.invoke({'nome': 'João'})

# Buscar por CPF parcial
resultados = search_patients.invoke({'cpf': '123'})

# Buscar com limite personalizado
resultados = search_patients.invoke({
    'nome': 'Silva',
    'limit': 20
})

print(f"Encontrados {resultados['total']} pacientes")
for paciente in resultados['pacientes']:
    print(f"- {paciente['nome']} (CPF: {paciente['cpf']})")
```

---

### 4. get_evolutions_for_attendance

Busca todas as evoluções clínicas de um atendimento específico.

**Parâmetros:**
- `atendimento_id` (int): ID do atendimento

**Retorno:**
Lista de dicionários com as evoluções:
- `id`: ID da evolução
- `tipo`: Tipo de evolução (Anamnese, Evolução Médica, etc.)
- `descricao`: Descrição da evolução
- `profissional`: Nome do profissional que registrou
- `data_hora`: Data e hora do registro

**Exemplo de uso:**

```python
from ia.services.tools import get_evolutions_for_attendance

evolucoes = get_evolutions_for_attendance(atendimento_id=5)

for evolucao in evolucoes:
    print(f"[{evolucao['data_hora']}] {evolucao['tipo']}")
    print(f"Profissional: {evolucao['profissional']}")
    print(f"Descrição: {evolucao['descricao']}\n")
```

---

## Integração com LangChain Agent

Para usar essas tools com um agente LangChain:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from ia.services.tools import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
)

# Configurar o modelo
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Lista de tools disponíveis
tools = [
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
]

# Prompt do sistema
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente médico especializado em consultar
    prontuários eletrônicos. Use as tools disponíveis para buscar informações
    sobre pacientes e seus atendimentos."""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Criar o agente
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Executar consulta
response = agent_executor.invoke({
    "input": "Busque o prontuário do paciente com CPF 12345678901 e me diga se ele tem alergias"
})

print(response["output"])
```

---

## Exemplos de Consultas em Linguagem Natural

Quando integrado com um LLM, o agente pode responder perguntas como:

1. **"Busque o prontuário do paciente João Silva"**
   - O agente usará `search_patients` para encontrar o ID e depois `get_patient_record_by_id`

2. **"Quais são as alergias do paciente com CPF 12345678901?"**
   - O agente usará `get_patient_record_by_cpf` e extrairá as alergias

3. **"Mostre o histórico completo de atendimentos do paciente ID 5"**
   - O agente usará `get_patient_record_by_id` com `include_attendance_history=True`

4. **"Quais evoluções foram registradas no atendimento 10?"**
   - O agente usará `get_evolutions_for_attendance`

5. **"Liste todos os pacientes com tipo sanguíneo O+"**
   - O agente pode buscar múltiplos pacientes e filtrar os resultados

---

## Estrutura de Dados Retornados

### Prontuário Completo (get_patient_record_by_id/cpf)

```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf": "12345678901",
  "data_nascimento": "01/01/1990",
  "sexo": "Masculino",
  "nome_mae": "Maria Silva",
  "telefone": "11999999999",
  "email": "joao@example.com",
  "documentos": {
    "rg": "123456789",
    "cartao_sus": "123456789012345"
  },
  "endereco": {
    "cep": "12345678",
    "rua": "Rua das Flores",
    "numero": "123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "uf": "SP",
    "endereco_completo": "Rua das Flores, nº 123, Centro, São Paulo/SP"
  },
  "dados_clinicos": {
    "tipo_sanguineo": "O+",
    "alergias": "Penicilina, amendoim",
    "observacoes_clinicas": "Hipertensão controlada"
  },
  "criado_em": "01/01/2025 10:00:00",
  "atualizado_em": "01/01/2025 15:30:00",
  "historico_atendimentos": [
    {
      "id": 5,
      "data_hora_entrada": "10/01/2025 14:00:00",
      "queixa": "Dor de cabeça",
      "status": "Alta",
      "profissional_responsavel": "Dr. Carlos (Médico)",
      "evolucoes": [
        {
          "id": 1,
          "tipo": "Anamnese",
          "descricao": "Paciente relata cefaleia há 2 dias...",
          "profissional": "Dr. Carlos (Médico)",
          "data_hora": "10/01/2025 14:15:00"
        }
      ]
    }
  ],
  "total_atendimentos": 1
}
```

---

## Segurança e Boas Práticas

1. **Validação de Dados**: Todas as tools validam os dados de entrada
2. **Tratamento de Erros**: Erros são capturados e retornados de forma estruturada
3. **Otimização de Queries**: Uso de `select_related()` para evitar N+1 queries
4. **Privacidade**: Nunca expor senhas ou dados sensíveis nas respostas
5. **Limites**: A tool `search_patients` limita os resultados a 50 por padrão

---

## Próximos Passos

Para expandir as funcionalidades, considere adicionar:

1. Tool para criar/atualizar evoluções clínicas
2. Tool para buscar sinais vitais (quando implementado na Fase 4)
3. Tool para buscar prescrições médicas (Fase 5)
4. Tool para solicitar/consultar exames (Fase 6)
5. Tool para gerar relatórios consolidados (Fase 7)

---

## Contato e Suporte

Para dúvidas ou sugestões, consulte a documentação principal em `CLAUDE.md` ou entre em contato com a equipe de desenvolvimento.

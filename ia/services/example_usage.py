"""
Exemplo de uso das tools LangChain para o Hospital Status Tracker

Este script demonstra como usar as tools criadas para buscar
informações de prontuários de pacientes.

IMPORTANTE: Execute este script dentro do contexto Django:
    python manage.py shell < ia/services/example_usage.py

Ou execute diretamente se o Django estiver configurado:
    python ia/services/example_usage.py
"""

import os
import django

# Configurar Django (necessário se executar fora do shell)
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

from ia.services.tools import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance
)


def exemplo_1_buscar_por_id():
    """Exemplo 1: Buscar prontuário por ID (apenas dados cadastrais)"""
    print("\n" + "="*80)
    print("EXEMPLO 1: Buscar prontuário por ID (dados cadastrais)")
    print("="*80)

    # Buscar paciente com ID 1
    resultado = get_patient_record_by_id.invoke({'paciente_id': 1})

    if 'error' in resultado:
        print(f"Erro: {resultado['error']}")
        return

    print(f"\n📋 Prontuário do Paciente")
    print(f"Nome: {resultado['nome']}")
    print(f"CPF: {resultado['cpf']}")
    print(f"Data de Nascimento: {resultado['data_nascimento']}")
    print(f"Sexo: {resultado['sexo']}")
    print(f"Telefone: {resultado['telefone']}")
    print(f"Email: {resultado['email']}")

    print(f"\n📄 Documentos")
    print(f"RG: {resultado['documentos']['rg']}")
    print(f"Cartão SUS: {resultado['documentos']['cartao_sus']}")

    print(f"\n📍 Endereço")
    print(f"{resultado['endereco']['endereco_completo']}")

    print(f"\n🏥 Dados Clínicos")
    print(f"Tipo Sanguíneo: {resultado['dados_clinicos']['tipo_sanguineo']}")
    print(f"Alergias: {resultado['dados_clinicos']['alergias']}")
    print(f"Observações: {resultado['dados_clinicos']['observacoes_clinicas']}")


def exemplo_2_buscar_com_historico():
    """Exemplo 2: Buscar prontuário com histórico completo"""
    print("\n" + "="*80)
    print("EXEMPLO 2: Buscar prontuário com histórico completo")
    print("="*80)

    # Buscar paciente com ID 1 incluindo histórico
    resultado = get_patient_record_by_id.invoke({
        'paciente_id': 1,
        'include_attendance_history': True
    })

    if 'error' in resultado:
        print(f"Erro: {resultado['error']}")
        return

    print(f"\n📋 Paciente: {resultado['nome']}")
    print(f"Total de atendimentos: {resultado.get('total_atendimentos', 0)}")

    if 'historico_atendimentos' in resultado:
        print(f"\n📅 Histórico de Atendimentos:")
        for atendimento in resultado['historico_atendimentos']:
            print(f"\n  Atendimento #{atendimento['id']}")
            print(f"  Data: {atendimento['data_hora_entrada']}")
            print(f"  Queixa: {atendimento['queixa']}")
            print(f"  Status: {atendimento['status']}")
            print(f"  Profissional: {atendimento['profissional_responsavel']}")

            if atendimento['evolucoes']:
                print(f"\n  📝 Evoluções Clínicas:")
                for evolucao in atendimento['evolucoes']:
                    print(f"    - [{evolucao['data_hora']}] {evolucao['tipo']}")
                    print(f"      Por: {evolucao['profissional']}")
                    print(f"      {evolucao['descricao'][:100]}...")
            else:
                print(f"  Sem evoluções registradas")


def exemplo_3_buscar_por_cpf():
    """Exemplo 3: Buscar prontuário por CPF"""
    print("\n" + "="*80)
    print("EXEMPLO 3: Buscar prontuário por CPF")
    print("="*80)

    # Buscar paciente por CPF (pode usar com ou sem formatação)
    cpf = "12345678901"  # Substitua por um CPF real do seu banco
    resultado = get_patient_record_by_cpf.invoke({'cpf': cpf})

    if 'error' in resultado:
        print(f"Erro: {resultado['error']}")
        return

    print(f"\n✅ Paciente encontrado!")
    print(f"Nome: {resultado['nome']}")
    print(f"CPF: {resultado['cpf']}")
    print(f"Tipo Sanguíneo: {resultado['dados_clinicos']['tipo_sanguineo']}")


def exemplo_4_buscar_pacientes():
    """Exemplo 4: Buscar pacientes por nome"""
    print("\n" + "="*80)
    print("EXEMPLO 4: Buscar pacientes por nome")
    print("="*80)

    # Buscar pacientes com "Silva" no nome
    resultado = search_patients.invoke({'nome': 'Silva', 'limit': 5})

    if 'error' in resultado:
        print(f"Erro: {resultado['error']}")
        return

    print(f"\n🔍 Encontrados {resultado['total']} pacientes")
    print(f"Exibindo {resultado['exibindo']} resultados:\n")

    for paciente in resultado['pacientes']:
        print(f"  ID: {paciente['id']}")
        print(f"  Nome: {paciente['nome']}")
        print(f"  CPF: {paciente['cpf']}")
        print(f"  Data Nascimento: {paciente['data_nascimento']}")
        print(f"  Sexo: {paciente['sexo']}")
        print(f"  Telefone: {paciente['telefone']}")
        print()


def exemplo_5_buscar_evolucoes():
    """Exemplo 5: Buscar evoluções de um atendimento"""
    print("\n" + "="*80)
    print("EXEMPLO 5: Buscar evoluções de um atendimento")
    print("="*80)

    # Buscar evoluções do atendimento ID 1
    evolucoes = get_evolutions_for_attendance(atendimento_id=1)

    if not evolucoes:
        print("Nenhuma evolução encontrada para este atendimento")
        return

    print(f"\n📝 Encontradas {len(evolucoes)} evoluções:\n")

    for evolucao in evolucoes:
        print(f"  [{evolucao['data_hora']}] {evolucao['tipo']}")
        print(f"  Profissional: {evolucao['profissional']}")
        print(f"  Descrição: {evolucao['descricao']}")
        print()


def exemplo_6_integracao_langchain():
    """Exemplo 6: Integração completa com LangChain Agent"""
    print("\n" + "="*80)
    print("EXEMPLO 6: Integração com LangChain Agent")
    print("="*80)

    print("""
    Para criar um agente LangChain completo, use o seguinte código:

    from langchain_openai import ChatOpenAI
    from langchain.agents import create_openai_functions_agent, AgentExecutor
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from ia.services.tools import (
        get_patient_record_by_id,
        get_patient_record_by_cpf,
        search_patients,
        get_evolutions_for_attendance
    )

    # Configurar o modelo (requer OPENAI_API_KEY)
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Lista de tools
    tools = [
        get_patient_record_by_id,
        get_patient_record_by_cpf,
        search_patients,
        get_evolutions_for_attendance
    ]

    # Prompt do sistema
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente médico especializado em consultar prontuários."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Criar e executar o agente
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Fazer perguntas em linguagem natural
    response = agent_executor.invoke({
        "input": "Busque o paciente João Silva e me diga se ele tem alergias"
    })

    print(response["output"])
    """)


def main():
    """Executa todos os exemplos"""
    print("\n" + "="*80)
    print("EXEMPLOS DE USO DAS TOOLS LANGCHAIN - HOSPITAL STATUS TRACKER")
    print("="*80)

    try:
        # Executar exemplos básicos
        exemplo_1_buscar_por_id()
        exemplo_2_buscar_com_historico()
        exemplo_3_buscar_por_cpf()
        exemplo_4_buscar_pacientes()
        exemplo_5_buscar_evolucoes()
        exemplo_6_integracao_langchain()

        print("\n" + "="*80)
        print("✅ Todos os exemplos foram executados!")
        print("="*80)
        print("\nPara mais informações, consulte: ia/services/TOOLS_USAGE.md")

    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

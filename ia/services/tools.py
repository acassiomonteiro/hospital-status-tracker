from langchain_core.tools import tool
from prontuario.models import Evolucao
from atendimentos.models import Atendimento
from pacientes.models import Paciente
from typing import Optional


def get_evolutions_for_attendance(atendimento_id: int) -> list:
    """
    Busca e retorna todas as evoluções clínicas para um atendimento específico.

    Args:
        atendimento_id (int): O ID do atendimento para o qual buscar as evoluções.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma evolução
              com seus detalhes (tipo, descrição, profissional, data/hora).
              Retorna uma lista vazia se nenhum atendimento ou evolução for encontrado.
    """
    try:
        atendimento = Atendimento.objects.get(id=atendimento_id)
        evolucoes = Evolucao.objects.filter(atendimento=atendimento).order_by('data_hora')
        
        result = []
        for evolucao in evolucoes:
            result.append({
                'id': evolucao.id,
                'tipo': evolucao.get_tipo_display(),
                'descricao': evolucao.descricao,
                'profissional': str(evolucao.profissional),
                'data_hora': evolucao.data_hora.strftime('%Y-%m-%d %H:%M:%S')
            })
        return result
    except Atendimento.DoesNotExist:
        return []
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error fetching evolutions for attendance {atendimento_id}: {e}")
        return []


def _get_patient_record(paciente_id: int, include_attendance_history: bool = False) -> dict:
    """
    Função auxiliar para buscar o prontuário completo de um paciente.
    Esta é uma função privada usada pelas tools públicas.
    """
    try:
        paciente = Paciente.objects.get(id=paciente_id)

        # Dados básicos e pessoais
        prontuario = {
            'id': paciente.id,
            'nome': paciente.nome,
            'cpf': paciente.cpf,
            'data_nascimento': paciente.data_nascimento.strftime('%d/%m/%Y'),
            'sexo': paciente.get_sexo_display() if paciente.sexo else None,
            'nome_mae': paciente.nome_mae,
            'telefone': paciente.telefone,
            'email': paciente.email,

            # Documentos
            'documentos': {
                'rg': paciente.rg,
                'cartao_sus': paciente.cartao_sus,
            },

            # Endereço
            'endereco': {
                'cep': paciente.cep,
                'rua': paciente.rua,
                'numero': paciente.numero,
                'bairro': paciente.bairro,
                'cidade': paciente.cidade,
                'uf': paciente.uf,
                'endereco_completo': paciente.get_endereco_completo(),
            },

            # Dados clínicos
            'dados_clinicos': {
                'tipo_sanguineo': paciente.tipo_sanguineo,
                'alergias': paciente.alergias,
                'observacoes_clinicas': paciente.observacoes_clinicas,
            },

            # Metadados
            'criado_em': paciente.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'atualizado_em': paciente.atualizado_em.strftime('%d/%m/%Y %H:%M:%S'),
        }

        # Incluir histórico de atendimentos se solicitado
        if include_attendance_history:
            atendimentos = Atendimento.objects.filter(paciente=paciente).select_related(
                'profissional_responsavel__user'
            ).order_by('-data_hora_entrada')

            historico = []
            for atendimento in atendimentos:
                atendimento_data = {
                    'id': atendimento.id,
                    'data_hora_entrada': atendimento.data_hora_entrada.strftime('%d/%m/%Y %H:%M:%S'),
                    'queixa': atendimento.queixa,
                    'status': atendimento.get_status_display(),
                    'profissional_responsavel': (
                        str(atendimento.profissional_responsavel)
                        if atendimento.profissional_responsavel
                        else 'Não atribuído'
                    ),
                    'evolucoes': []
                }

                # Buscar evoluções do atendimento
                evolucoes = Evolucao.objects.filter(atendimento=atendimento).select_related(
                    'profissional__user'
                ).order_by('data_hora')

                for evolucao in evolucoes:
                    atendimento_data['evolucoes'].append({
                        'id': evolucao.id,
                        'tipo': evolucao.get_tipo_display(),
                        'descricao': evolucao.descricao,
                        'profissional': str(evolucao.profissional),
                        'data_hora': evolucao.data_hora.strftime('%d/%m/%Y %H:%M:%S')
                    })

                historico.append(atendimento_data)

            prontuario['historico_atendimentos'] = historico
            prontuario['total_atendimentos'] = len(historico)

        return prontuario

    except Paciente.DoesNotExist:
        return {'error': f'Paciente com ID {paciente_id} não encontrado'}
    except Exception as e:
        print(f"Error fetching patient record for ID {paciente_id}: {e}")
        return {'error': f'Erro ao buscar prontuário: {str(e)}'}


@tool
def get_patient_record_by_id(paciente_id: int, include_attendance_history: bool = False) -> dict:
    """
    Busca e retorna o prontuário completo de um paciente pelo ID.

    Args:
        paciente_id (int): O ID do paciente para buscar o prontuário.
        include_attendance_history (bool): Se True, inclui histórico completo de atendimentos e evoluções.
                                          Default: False (retorna apenas dados cadastrais).

    Returns:
        dict: Dicionário com todos os dados do prontuário do paciente, incluindo:
              - Dados pessoais (nome, CPF, data de nascimento, sexo, etc.)
              - Documentos (RG, Cartão SUS)
              - Endereço completo
              - Dados clínicos (tipo sanguíneo, alergias, observações)
              - Histórico de atendimentos (se solicitado)

        Retorna dicionário vazio se o paciente não for encontrado.
    """
    return _get_patient_record(paciente_id, include_attendance_history)


@tool
def get_patient_record_by_cpf(cpf: str, include_attendance_history: bool = False) -> dict:
    """
    Busca e retorna o prontuário completo de um paciente pelo CPF.

    Args:
        cpf (str): O CPF do paciente (apenas números, 11 dígitos).
        include_attendance_history (bool): Se True, inclui histórico completo de atendimentos e evoluções.
                                          Default: False (retorna apenas dados cadastrais).

    Returns:
        dict: Dicionário com todos os dados do prontuário do paciente, incluindo:
              - Dados pessoais (nome, CPF, data de nascimento, sexo, etc.)
              - Documentos (RG, Cartão SUS)
              - Endereço completo
              - Dados clínicos (tipo sanguíneo, alergias, observações)
              - Histórico de atendimentos (se solicitado)

        Retorna dicionário com erro se o paciente não for encontrado.
    """
    try:
        # Remover caracteres não numéricos do CPF
        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        if len(cpf_limpo) != 11:
            return {'error': 'CPF deve conter exatamente 11 dígitos numéricos'}

        # Buscar paciente pelo CPF
        paciente = Paciente.objects.get(cpf=cpf_limpo)

        # Reutilizar a função auxiliar
        return _get_patient_record(paciente.id, include_attendance_history)

    except Paciente.DoesNotExist:
        return {'error': f'Paciente com CPF {cpf} não encontrado'}
    except Exception as e:
        print(f"Error fetching patient record for CPF {cpf}: {e}")
        return {'error': f'Erro ao buscar prontuário: {str(e)}'}


@tool
def search_patients(nome: Optional[str] = None, cpf: Optional[str] = None, limit: int = 10) -> dict:
    """
    Busca pacientes por nome ou CPF (busca parcial).

    Args:
        nome (str, optional): Nome ou parte do nome do paciente para buscar.
        cpf (str, optional): CPF ou parte do CPF do paciente para buscar.
        limit (int): Número máximo de resultados a retornar (default: 10, máximo: 50).

    Returns:
        dict: Dicionário contendo:
              - 'total': Número total de pacientes encontrados
              - 'pacientes': Lista de pacientes com dados básicos (id, nome, cpf, data_nascimento)

        Se nenhum critério de busca for fornecido, retorna os últimos pacientes cadastrados.
    """
    try:
        # Validar limite
        if limit > 50:
            limit = 50

        # Query base
        query = Paciente.objects.all()

        # Aplicar filtros
        if nome:
            query = query.filter(nome__icontains=nome)

        if cpf:
            # Remover caracteres não numéricos do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            query = query.filter(cpf__icontains=cpf_limpo)

        # Ordenar por mais recente
        query = query.order_by('-criado_em')

        # Contar total
        total = query.count()

        # Limitar resultados
        pacientes = query[:limit]

        # Formatar resultado
        resultado = {
            'total': total,
            'exibindo': len(pacientes),
            'pacientes': []
        }

        for paciente in pacientes:
            resultado['pacientes'].append({
                'id': paciente.id,
                'nome': paciente.nome,
                'cpf': paciente.cpf,
                'data_nascimento': paciente.data_nascimento.strftime('%d/%m/%Y'),
                'sexo': paciente.get_sexo_display() if paciente.sexo else 'Não informado',
                'telefone': paciente.telefone or 'Não informado',
            })

        return resultado

    except Exception as e:
        print(f"Error searching patients: {e}")
        return {'error': f'Erro ao buscar pacientes: {str(e)}'}

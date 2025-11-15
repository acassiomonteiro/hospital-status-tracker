"""
Testes para as tools LangChain

Execute com: python manage.py test ia.services.test_tools
"""

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from pacientes.models import Paciente
from usuarios.models import Profissional
from atendimentos.models import Atendimento
from prontuario.models import Evolucao
from ia.services.tools import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance,
)


class PatientToolsTestCase(TestCase):
    """Testes para as tools de busca de pacientes"""

    def setUp(self):
        """Configurar dados de teste"""
        # Criar usuário e profissional
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profissional = Profissional.objects.create(
            user=self.user,
            perfil='MEDICO',
            registro_profissional='CRM12345'
        )

        # Criar paciente de teste
        self.paciente = Paciente.objects.create(
            nome='João da Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            sexo='M',
            telefone='11999999999',
            email='joao@test.com',
            tipo_sanguineo='O+',
            alergias='Penicilina',
            rua='Rua Teste',
            numero='123',
            cidade='São Paulo',
            uf='SP'
        )

        # Criar atendimento
        self.atendimento = Atendimento.objects.create(
            paciente=self.paciente,
            profissional_responsavel=self.profissional,
            queixa='Dor de cabeça',
            status='TRIAGEM'
        )

        # Criar evolução
        self.evolucao = Evolucao.objects.create(
            atendimento=self.atendimento,
            profissional=self.profissional,
            tipo='ANAMNESE',
            descricao='Paciente relata cefaleia há 2 dias'
        )

    def test_get_patient_record_by_id_basic(self):
        """Testar busca de prontuário por ID (dados básicos)"""
        resultado = get_patient_record_by_id.invoke({'paciente_id': self.paciente.id})

        self.assertNotIn('error', resultado)
        self.assertEqual(resultado['nome'], 'João da Silva')
        self.assertEqual(resultado['cpf'], '12345678901')
        self.assertEqual(resultado['dados_clinicos']['tipo_sanguineo'], 'O+')
        self.assertEqual(resultado['dados_clinicos']['alergias'], 'Penicilina')

    def test_get_patient_record_by_id_with_history(self):
        """Testar busca de prontuário por ID com histórico"""
        resultado = get_patient_record_by_id.invoke({
            'paciente_id': self.paciente.id,
            'include_attendance_history': True
        })

        self.assertNotIn('error', resultado)
        self.assertIn('historico_atendimentos', resultado)
        self.assertEqual(resultado['total_atendimentos'], 1)
        self.assertEqual(len(resultado['historico_atendimentos'][0]['evolucoes']), 1)

    def test_get_patient_record_by_id_not_found(self):
        """Testar busca de paciente inexistente por ID"""
        resultado = get_patient_record_by_id.invoke({'paciente_id': 99999})

        self.assertIn('error', resultado)

    def test_get_patient_record_by_cpf(self):
        """Testar busca de prontuário por CPF"""
        resultado = get_patient_record_by_cpf.invoke({'cpf': '12345678901'})

        self.assertNotIn('error', resultado)
        self.assertEqual(resultado['nome'], 'João da Silva')

    def test_get_patient_record_by_cpf_formatted(self):
        """Testar busca de prontuário por CPF formatado"""
        resultado = get_patient_record_by_cpf.invoke({'cpf': '123.456.789-01'})

        self.assertNotIn('error', resultado)
        self.assertEqual(resultado['nome'], 'João da Silva')

    def test_get_patient_record_by_cpf_invalid(self):
        """Testar busca com CPF inválido"""
        resultado = get_patient_record_by_cpf.invoke({'cpf': '123'})

        self.assertIn('error', resultado)

    def test_search_patients_by_name(self):
        """Testar busca de pacientes por nome"""
        resultado = search_patients.invoke({'nome': 'João'})

        self.assertNotIn('error', resultado)
        self.assertGreaterEqual(resultado['total'], 1)
        self.assertGreater(len(resultado['pacientes']), 0)

    def test_search_patients_by_cpf(self):
        """Testar busca de pacientes por CPF parcial"""
        resultado = search_patients.invoke({'cpf': '123'})

        self.assertNotIn('error', resultado)
        self.assertGreaterEqual(resultado['total'], 1)

    def test_search_patients_with_limit(self):
        """Testar busca de pacientes com limite"""
        # Criar mais pacientes
        for i in range(15):
            Paciente.objects.create(
                nome=f'Paciente Teste {i}',
                cpf=f'1234567890{i:02d}',
                data_nascimento=date(1990, 1, 1)
            )

        resultado = search_patients.invoke({'limit': 5})

        self.assertLessEqual(resultado['exibindo'], 5)

    def test_get_evolutions_for_attendance(self):
        """Testar busca de evoluções de um atendimento"""
        evolucoes = get_evolutions_for_attendance(self.atendimento.id)

        self.assertEqual(len(evolucoes), 1)
        self.assertEqual(evolucoes[0]['tipo'], 'Anamnese')
        self.assertEqual(evolucoes[0]['descricao'], 'Paciente relata cefaleia há 2 dias')

    def test_get_evolutions_for_nonexistent_attendance(self):
        """Testar busca de evoluções de atendimento inexistente"""
        evolucoes = get_evolutions_for_attendance(99999)

        self.assertEqual(len(evolucoes), 0)

    def test_patient_with_multiple_attendances(self):
        """Testar paciente com múltiplos atendimentos"""
        # Criar mais atendimentos
        for i in range(3):
            atendimento = Atendimento.objects.create(
                paciente=self.paciente,
                profissional_responsavel=self.profissional,
                queixa=f'Queixa {i}',
                status='TRIAGEM'
            )
            Evolucao.objects.create(
                atendimento=atendimento,
                profissional=self.profissional,
                tipo='EVOLUCAO_MEDICA',
                descricao=f'Evolução {i}'
            )

        resultado = get_patient_record_by_id.invoke({
            'paciente_id': self.paciente.id,
            'include_attendance_history': True
        })

        self.assertEqual(resultado['total_atendimentos'], 4)  # 1 original + 3 novos

    def test_tool_invoke_compatibility(self):
        """Testar compatibilidade com a interface invoke do LangChain"""
        # Verificar se as tools têm o método invoke
        self.assertTrue(hasattr(get_patient_record_by_id, 'invoke'))
        self.assertTrue(hasattr(get_patient_record_by_cpf, 'invoke'))
        self.assertTrue(hasattr(search_patients, 'invoke'))

        # Testar invocação
        resultado = get_patient_record_by_id.invoke({'paciente_id': self.paciente.id})
        self.assertIsInstance(resultado, dict)


class ToolsIntegrationTestCase(TestCase):
    """Testes de integração para verificar o fluxo completo"""

    def setUp(self):
        """Configurar dados de teste"""
        self.user = User.objects.create_user(username='doctor', password='pass123')
        self.profissional = Profissional.objects.create(
            user=self.user,
            perfil='MEDICO'
        )

        self.paciente = Paciente.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1985, 5, 15),
            alergias='Dipirona, Látex',
            observacoes_clinicas='Diabética tipo 2'
        )

    def test_complete_workflow(self):
        """Testar fluxo completo: buscar paciente, verificar alergias"""
        # 1. Buscar paciente por nome
        busca = search_patients.invoke({'nome': 'Maria'})
        self.assertGreater(busca['total'], 0)

        # 2. Obter ID do primeiro resultado
        paciente_id = busca['pacientes'][0]['id']

        # 3. Buscar prontuário completo
        prontuario = get_patient_record_by_id.invoke({'paciente_id': paciente_id})

        # 4. Verificar alergias
        self.assertIn('Dipirona', prontuario['dados_clinicos']['alergias'])
        self.assertIn('Diabética', prontuario['dados_clinicos']['observacoes_clinicas'])

    def test_cpf_search_and_details(self):
        """Testar busca por CPF e obtenção de detalhes"""
        # Buscar por CPF
        prontuario = get_patient_record_by_cpf.invoke({'cpf': '98765432100'})

        self.assertEqual(prontuario['nome'], 'Maria Santos')
        self.assertEqual(prontuario['dados_clinicos']['alergias'], 'Dipirona, Látex')

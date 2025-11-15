"""
Serviços de IA para o Hospital Status Tracker

Este módulo contém ferramentas LangChain para consulta de prontuários
e integração com agentes de IA.
"""

from .tools import (
    get_patient_record_by_id,
    get_patient_record_by_cpf,
    search_patients,
    get_evolutions_for_attendance,
)

__all__ = [
    'get_patient_record_by_id',
    'get_patient_record_by_cpf',
    'search_patients',
    'get_evolutions_for_attendance',
]

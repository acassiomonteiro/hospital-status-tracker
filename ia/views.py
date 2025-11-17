"""
Views para o app de Inteligncia Artificial (ia).
"""
# TEMPORARIAMENTE DESABILITADO - módulos ia.services foram removidos
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_http_methods

# from atendimentos.models import Atendimento
# from ia.services.tools import get_patient_record_by_id
# from ia.services.summarizer import generate_summary

# @login_required
# @require_http_methods(["GET"])
# def resumir_prontuario_view(request, atendimento_id):
#     """
#     View que gera e retorna um resumo de pronturio via IA.
#     """
#     try:
#         # 1. Buscar o atendimento para obter o ID do paciente
#         atendimento = Atendimento.objects.select_related('paciente').get(id=atendimento_id)
#         paciente_id = atendimento.paciente.id

#         # 2. Obter os dados completos do pronturio usando a tool existente
#         # Usamos include_attendance_history=True para dar o contexto completo para a IA
#         prontuario_data = get_patient_record_by_id.invoke({
#             'paciente_id': paciente_id,
#             'include_attendance_history': True
#         })

#         if 'error' in prontuario_data:
#             return JsonResponse({'error': prontuario_data['error']}, status=404)

#         # 3. Gerar o resumo com o servio de IA
#         summary = generate_summary(prontuario_data)

#         # 4. Retornar o resumo como JSON
#         return JsonResponse({'summary': summary})

#     except Atendimento.DoesNotExist:
#         return JsonResponse({'error': 'Atendimento no encontrado.'}, status=404)
#     except Exception as e:
#         # Log do erro seria ideal aqui
#         print(f"Erro inesperado na view resumir_prontuario_view: {e}")
#         return JsonResponse({'error': f'Ocorreu um erro interno: {str(e)}'}, status=500)
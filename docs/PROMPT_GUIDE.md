# PROMPT_GUIDE.md
Guia de Estrutura para Prompts Técnicos — *Hospital Status Tracker*

Este documento serve como **referência para escrever prompts claros, objetivos e reutilizáveis** durante o desenvolvimento do sistema.  
Ele define **como escrever**, não **o que executar**.  
Use-o apenas como apoio para novas fases ou implementações (não cole inteiro em um prompt de código).

---

## Filosofia: Vibe Coding
Os prompts devem tratar o modelo como um **dev sênior**, não como um estagiário.

**Você define:**
- O **objetivo** (o que deve existir e por quê);
- O **contexto** (onde será implementado);
- As **restrições e padrões** (para manter consistência);
- O **resultado esperado** (como validar).

**O modelo decide:**  
- Como estruturar o código,
- Quais boas práticas aplicar,
- Como integrar com o sistema existente.

---

## Estrutura Recomendada

Use este formato como base ao criar cada prompt técnico:

```
OBJETIVO:
Explique em 1–2 frases o propósito da implementação e o resultado desejado.

CONTEXTO:
- Descreva o ambiente técnico (ex.: Django 5, dockerizado, CBVs).
- Liste os models, views ou templates afetados.
- Indique dependências existentes (autenticação, relacionamentos etc.).
- Cite padrões do projeto (ex.: CLAUDE.md).

TAREFA:
- Liste as ações principais em alto nível (sem detalhar como fazer).
- Agrupe por domínio se necessário (models, forms, views, templates).
- Inclua choices ou relacionamentos específicos se forem parte da regra de negócio.

PADRÕES:
- Regras e boas práticas do projeto (CBVs, Tailwind, português).
- Requisitos de compatibilidade ou validação.
- Convenções visuais ou de código a seguir.

NÃO FAZER:
- Liste o que deve ser evitado para limitar o escopo.
- Exemplo: "Não criar novos apps", "Não adicionar JS complexo".

SAÍDA ESPERADA:
- O tipo de resultado desejado (código atualizado, migrations, commits, exemplos de teste).
```

---

## Exemplo Real de Uso

### Prompt — *Fase 3: Evoluções Clínicas*

```
OBJETIVO:
Implementar sistema de registro de evoluções clínicas, permitindo que profissionais documentem a progressão do atendimento ao longo do tempo.

CONTEXTO:
- Projeto Django 5 dockerizado.
- Models existentes: Paciente, Atendimento, Profissional.
- Autenticação implementada (request.user.profissional).
- Templates base com Tailwind (base.html, dashboard.html).
- Padrões definidos em CLAUDE.md.

TAREFA:
- Criar Model Evolucao vinculado a Atendimento e Profissional.
- Adicionar campo tipo (choices: ANAMNESE, EVOLUCAO_MEDICA, EVOLUCAO_ENFERMAGEM, EXAME_FISICO).
- Criar Form e View para adicionar e listar evoluções.
- Atualizar template de atendimento com seção de evoluções e botão "Adicionar Evolução".

PADRÕES:
- Profissional vinculado automaticamente (request.user.profissional).
- Data/hora auto_now_add=True.
- Timeline order_by('-data_hora').
- Layout com cores diferentes por tipo de evolução.
- Labels e verbose_name em português.

NÃO FAZER:
- Não criar sistema de edição de evoluções.
- Não adicionar rich text editor.
- Não adicionar permissões complexas por tipo de profissional.

SAÍDA ESPERADA:
- Código atualizado em models.py, views.py, urls.py, forms.py e templates.
- Exemplo via shell para teste.
- Sugestão de commit (conventional commits).
- Lista de rotas adicionadas.
```

---

## Dicas rápidas
- 200–250 palavras é o **tamanho ideal**.  
- Evite verbos prescritivos como “adicione”, “importe” — use “implemente”, “crie”, “integre”.  
- Dê **liberdade para o modelo decidir como**, mas **clareza sobre o que**.  
- Detalhe apenas **regras de negócio** específicas (não sintaxe Django).  
- Sempre termine com **SAÍDA ESPERADA**, para garantir entregas verificáveis.  

---

### Em resumo:
> “Você define o mapa. O modelo dirige.”

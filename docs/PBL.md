VISÃO DA UNDB
Ser uma instituição nacionalmente reconhecida pela sua excelência em todas as suas
áreas de atuação.
MISSÃO DA UNDB
Promover o conhecimento alicerçado em princípios éticos, científicos e tecnológicos,
através de metodologias de vanguarda, visando à formação e ao aperfeiçoamento
humano de profissionais comprometidos com o processo de desenvolvimento e
mudança nos seus campos de atuação.
1 INFORMAÇÕES SOBRE O COMPONENTE CURRICULAR
Disciplina: Programação para Web Carga Horária: 68 h
Professor: Esp. Guilherme Ferreira dos Reis Turno: Matutino
Curso: Escola de Tecnologia Período/Semestre: 5º Módulo
O Hospital Santa Helena Norte é referência regional em atenção de média
complexidade, operando pronto-socorro ininterrupto, UTI adulto e neonatal, centro de
diagnóstico por imagem e laboratório clínico. A pressão por desfechos assistenciais e
equilíbrio econômico convive com histórico de sistemas heterogêneos e processos
parcialmente digitalizados. À medida que a demanda cresce e a exigência regulatória se
intensifica, tornam-se mais visíveis as lacunas de continuidade do registro clínico e de
visibilidade sobre o status assistencial no ponto de cuidado.
A estrutura física compreende 220 leitos distribuídos entre clínica médica,
cirúrgica e pediatria, com picos de ocupação que tensionam o giro de leitos. O corpo clínico é
composto por equipes fixas e plantonistas, enquanto a enfermagem subdivide-se em
unidades com rotinas e nomenclaturas próprias. A TI mantém dois servidores legados, com
banco de dados on-premise, contingências pouco exercitadas e monitoramento reativo. Há
processos de auditoria interna, porém dependentes de documentação dispersa.
O ingresso do paciente pelo pronto-socorro inicia com triagem e classificação de
risco. A partir daí, sucedem-se consultas, prescrições, evoluções e solicitações de exames.
Parte das etapas é registrada em prontuário físico, outra parte em aplicação ambulatorial sem
integração formal com diagnóstico por imagem e laboratório; em setores específicos,
planilhas auxiliares capturam informações operacionais para “agilizar” comunicação entre

turnos. Ao final, o prontuário do mesmo episódio clínico pode existir como combinação de
papel, telas do legado e arquivos externos, cada um com temporalidade e granularidade
distintas.
Os resultados de exames laboratoriais e de imagem, por vezes, são
disponibilizados em portais de terceiros, com notificações enviadas por e-mail a endereços
genéricos de setor. Quando recebidos, podem ser impressos, anexados ao prontuário físico
ou resumidos manualmente em campos livres do sistema ambulatorial. Em situações de
downtime ou de sobrecarga, plantões adotam procedimentos alternativos, como mensagens
por aplicativos não institucionais para sinalização de achados relevantes. O efeito prático é a
coexistência de múltiplos “locais de verdade”, em que o dado clínico circula sem trilha de
auditoria consolidada.
A ocupação e o status do paciente (triagem, em atendimento, aguardando exame,
em exame, aguardando resultado, alta, internação) são atualizados de forma não uniforme
entre as unidades. Quadros brancos físicos, planilhas e comunicados verbais produzem
instantâneos que rapidamente se desatualizam. Em horários de maior fluxo, a divergência
entre o que consta no quadro, o que está no papel e o que se vê na aplicação legada torna-se
crítica para a decisão clínica e a logística de leitos.
Não é incomum a existência de cadastros com grafias distintas para o mesmo
paciente, variações de CPF, ou reaproveitamento de cadastro por semelhança. Em episódios
de cuidado recorrentes, o vínculo inequívoco entre consulta, prescrição e pedido de exame
pode se perder, dificultando a reconstituição da linha do tempo: quando e por quem
determinado status foi alterado; qual solicitação gerou qual resultado; e quais pendências
permanecem impeditivas para decisão de alta.
Os servidores executam versões antigas de sistema operacional e SGBD; há rotinas
de cópia de segurança, porém nem sempre auditadas por restaurações periódicas. Logs
encontram-se distribuídos entre aplicações e arquivos locais, com baixa centralização e pouca
capacidade de correlação de eventos. Tentativas de integração com fornecedores externos
seguem arranjos ad hoc, sem contrato de interoperabilidade, documentação completa ou
aderência consistente a padrões. Em picos de demanda, a degradação de desempenho torna
a experiência do usuário instável.
Há lacunas na atribuição de responsabilidade individual por ação registrada. Em
diversos setores, credenciais genéricas são compartilhadas por turno, inviabilizando

rastreabilidade confiável. As trilhas de auditoria são incompletas para responder a perguntas
simples: que profissional alterou determinado registro; qual a versão válida de um laudo; que
transição de status ocorreu entre dois horários. A aderência a princípios de privacy by design
é desigual, e políticas de acesso nem sempre refletem a necessidade de segregação por perfil.
Em auditorias, emergem divergências entre o que foi prescrito, o que foi
efetivamente coletado, o que foi laudo liberado e o que está visível no ponto de cuidado. Em
alta médica, persistem pendências não estruturadas de exames relevantes, que podem
reaparecer como reconsulta em curto intervalo. Para o faturamento, a comprovação do nexo
entre atendimento, solicitação e resultado nem sempre é trivially reconstituível, alimentando
glosas e prazos de recebimento dilatados. Para a equipe assistencial, a ausência de um eixo
narrativo único do episódio de cuidado impõe retrabalho cognitivo e administrativo.
A direção monitora tempo médio de permanência, taxa de reconsulta em 72
horas, pendência de laudos e ocupação de leitos, mas os números refletem variações por
fonte de dados e por método de consolidação. Plantões relatam “zonas cinzentas” de
responsabilidade nos momentos de transição (admissão, transferência, alta), quando registros
simultâneos e incompletos convergem para decisões com impacto clínico e operacional. O
risco percebido combina fatores informacionais, tecnológicos e comportamentais.
A narrativa vigente descreve um hospital com capacidade instalada e expertise
clínica consolidadas, tensionado por ecossistema informacional fragmentado. O itinerário do
paciente se vê atravessado por descontinuidades de registro, múltiplas representações do
mesmo fato assistencial e ausência de visibilidade consolidada do status ao longo do tempo.
A instituição experimenta, ao mesmo tempo, exigências de eficiência e de segurança do
paciente, enquanto opera sobre infraestrutura legada, integrações incertas e práticas
documentais heterogêneas entre setores.
Sem prescrever soluções, observa-se que a problemática envolve identidade
inequívoca do paciente e do episódio, vínculo consistente entre eventos clínicos,
reconstituição confiável da linha do tempo e visibilidade operacional do status em unidades
com ritmos distintos. Permanecem abertas questões sobre como representar, sustentar e
auditar o curso do cuidado sem interromper a assistência, como compatibilizar vocabulários
setoriais e como alinhar registros às necessidades clínicas, gerenciais e regulatórias. As
respostas demandam compreensão aprofundada do cenário descrito, análise crítica das
dependências e proposições que considerem as restrições e tensões aqui delineadas.
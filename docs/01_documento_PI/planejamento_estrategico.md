# Planejamento Estratégico & Gestão Organizacional
## Nova DPS Informática - Projeto Integrador I

Este documento consolida as análises de macroambiente, diagnóstico interno e planejamento tático exigidas pelas disciplinas de **Análise do Ambiente e Gestão da Informação** (Prof. Márcio Fontoura) e **Administração Geral** (Prof. Márcio Camarotto).

---

## 1. Análise PESTEL (Macroambiente)

A análise PESTEL avalia os fatores externos que afetam diretamente as operações e a tomada de decisão da Nova DPS Informática:

| Dimensão | Fatores Relevantes | Impacto no Negócio |
|---|---|---|
| **Político** | Políticas de incentivo à reciclagem de lixo eletrônico (REEE) e normas de descarte sustentável de baterias e placas de circuito. | Necessidade de descarte ecológico certificado para placas condenadas. |
| **Econômico** | Alta volatilidade cambial (dólar alto encarece componentes e novos computadores); inflação acumulada. | Aumento na procura por conserto em vez de compra de novos equipamentos; encarecimento de semicondutores importados. |
| **Social** | Dependência crítica de home office e estudos remotos; consumidores mais exigentes com prazos de entrega. | Maior tolerância a preços mais altos, desde que o tempo de reparo seja mínimo e haja garantia. |
| **Tecnológico** | Miniaturização de circuitos, soldagem BGA sem chumbo, chips soldados em placas-mãe (ex: Apple Silicon, ultrabooks). | Exigência de ferramental avançado (estações infravermelho de reballing e osciloscópios) e técnicos qualificados. |
| **Ecológico / Ambiental** | Conscientização sobre a vida útil dos eletrônicos e economia circular. | Posicionamento da assistência como promotora da extensão da vida útil de ativos de TI. |
| **Legal** | Lei Geral de Proteção de Dados (LGPD - Lei 13.709/2018) e Código de Defesa do Consumidor (Art. 26 - garantia legal de 90 dias). | Rigor absoluto no sigilo dos dados presentes nos discos dos clientes durante testes de bancada. |

---

## 2. Metas SMART e Indicadores de Performance (KPIs)

Definidas para o horizonte de 6 meses pós-implantação do software:

1. **Meta 1 (Redução de Tempo de Reparo - TAT):**
   - **S (Específica):** Diminuir o tempo médio de reparo de notebooks e desktops na bancada.
   - **M (Mensurável):** De 5,5 dias para no máximo 2,5 dias úteis.
   - **A (Atingível):** Possível graças à fila ordenada de serviços pendentes e estoque prévio de insumos críticos.
   - **R (Relevante):** É o principal critério de satisfação e fidelização dos clientes corporativos e finais.
   - **T (Temporal):** Alcançar a meta em 90 dias após a entrada do sistema em produção.

2. **Meta 2 (Aumento de Faturamento por Rastreio de Peças):**
   - **S (Específica):** Aumentar o faturamento bruto mensal através do controle das margens de peças alocadas.
   - **M (Mensurável):** Crescimento de 20% no faturamento bruto (de R$ 25.000 para R$ 30.000 mensais).
   - **A (Atingível):** Fim do desperdício de peças não cobradas nos orçamentos finais.
   - **R (Relevante):** Sustentabilidade financeira e ampliação do laboratório técnico.
   - **T (Temporal):** Atingir em 6 meses.

3. **Meta 3 (Eliminação de Inadimplência em Chamados Concluídos):**
   - **S (Específica):** Reduzir a taxa de pedidos entregues sem a quitação integral registrada.
   - **M (Mensurável):** Taxa de inadimplência de pedidos concluídos menor que 2%.
   - **A (Atingível):** Travamento de entrega no sistema enquanto houver saldo devedor na tabela de pagamentos.
   - **R (Relevante):** Manutenção do fluxo de caixa operacional.
   - **T (Temporal):** Nos primeiros 30 dias de uso.

---

## 3. Plano de Ação 5W2H

| O quê (What)? | Por quê (Why)? | Onde (Where)? | Quem (Who)? | Quando (When)? | Como (How)? | Quanto (How Much)? |
|---|---|---|---|---|---|---|
| **Implantar o Sistema Desktop Nova DPS** | Eliminar controles manuais e desvios de peças. | Recepção e Laboratório Técnico. | Equipe de TI do PI. | Mês 1 - Semana 3. | Instalação do app PySide6 nos terminais de atendimento e bancada. | Custo zero (projeto acadêmico / open source). |
| **Treinar Equipe nos Procedimentos de OS** | Garantir que 100% dos chamados e peças sejam registrados. | Sala de Reuniões da Nova DPS. | Alunos do PI e Gerente Técnico. | Mês 2 - Semana 1. | Workshop prático de 4 horas simulando abertura, reparo e baixa de estoque. | R$ 200,00 (material instrucional e coffee break). |
| **Integrar Exportação com Dashboard Power BI** | Apoiar a tomada de decisão da diretoria com métricas visuais. | Diretoria / Gerência. | Alunos responsáveis pelo BI. | Mês 2 - Semana 3. | Importação dos CSVs estrela e publicação do relatório analítico. | Sem custo adicional de licenciamento. |
| **Auditar Margens de Lucro de Fornecedores** | Identificar quais fornecedores entregam melhor custo-benefício. | Setor de Compras. | Gestor da Nova DPS. | Mês 3 (Mensalmente). | Relatório analítico de peças e margens gerado pelo sistema. | Tempo operacional de 2 horas/mês. |

---

## 4. Recursos Necessários e Cronograma de Execução

### Recursos:
- **Humanos:** 5 Desenvolvedores/Analistas (Grupo de alunos do PI), 1 Gerente Técnico da Nova DPS, 2 Técnicos de bancada.
- **Materiais & Hardware:** 2 Computadores de bancada (Core i5, 8GB RAM), 1 Notebook de atendimento, roteador local.
- **Tecnológicos/Software:** Python 3, PySide6, PostgreSQL/SQLite, SQLAlchemy, Power BI Desktop, Git/GitHub.

### Cronograma de Marcos (Milestones):
- **Semana 1-2:** Levantamento de requisitos, Análise de Ambiente (SWOT/PESTEL) e Modelagem E-R.
- **Semana 3-4:** Criação do script DDL, normalização e carga inicial com dados sintéticos (100+ registros).
- **Semana 5-6:** Desenvolvimento dos serviços de backend e consultas analíticas de fila e balanço.
- **Semana 7-8:** Construção da interface gráfica Fluent Design em PySide6 e integração dos CRUDs.
- **Semana 9-10:** Exportação em Esquema Estrela e montagem do painel no Power BI.
- **Semana 11-12:** Testes automatizados de software, homologação e elaboração da documentação final.

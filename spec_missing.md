# Especificação de Funcionalidades Faltantes

## 1. Modelos de Dados & Script de Criação do Banco
- `schema.sql` contendo a definição completa das tabelas (`cliente`, `pedido`, `servico`, `orcamento`, `peca`, `pagamento`) com chaves primárias/estrangeiras.
- `seed.sql` opcional para popular dados de exemplo.
- Atualizar `conexao_db.py` para validar a existência do banco e executar o script de criação caso ele não exista.

## 2. UI Estética
- Migrar de **PySimpleGUI** para um framework com suporte a estilos avançados (ex.: **PyQt6**, **Streamlit**, **DearPyGui**).
- Definir paleta de cores, tipografia e ícones. 
- Implementar layouts responsivos e componentes de navegação modernos.

## 3. Relatórios Operacionais
- Consultas SQL avançadas para: 
  - Fila de Serviços Pendentes (ordenada por tempo de espera).
  - Balanço Financeiro (valor cobrado vs. pago).
  - Rastreabilidade de peças por equipamento.
- Exportar resultados para CSV/Excel.
- Exibir tabelas interativas na nova UI.

## 4. Dashboard Power BI
- Criar arquivo `dashboard.pbix` que consuma os datasets exportados (CSV ou conexão direta ao PostgreSQL).
- Documentar o processo de atualização do dataset.

## 5. Backlog / Planejamento de Sprints
- `backlog.md` contendo lista de requisitos funcionais e não‑funcionais, priorizados por valor de negócio.
- Definir sprints curtas (2‑3 semanas) com entregáveis claros.

## 6. Testes Automatizados & CI
- Estrutura de testes com **pytest** para camada de acesso ao DB e lógica de negócios.
- Workflow GitHub Actions (`.github/workflows/ci.yml`) que:
  - Instala dependências.
  - Executa testes.
  - Gera artefatos de documentação.

## 7. Documentação Complementar
- `README.md` ampliado com:
  - Guia de configuração (ex.: `.env.example`).
  - Instruções para inicializar o banco (`psql -f schema.sql`).
  - Como rodar a UI nova.
- `docs/` contendo diagramas ER (PNG) gerados com `erdantic` ou outra ferramenta.

## 8. Segurança & Configurações
- Utilizar `python-dotenv` para carregar variáveis sensíveis.
- Validar/escapar inputs de usuários nas queries (usar parâmetros nomeados como já feito).

---

**Próximos Passos**
1. Criar a estrutura de diretórios (`docs/`, `scripts/`, `tests/`).
2. Implementar `schema.sql` e `seed.sql`.
3. Inicializar repositório Git e fazer o primeiro commit contendo a especificação acima e a estrutura base.
4. Escolher o framework UI (recomendação: PyQt6) e instalar dependências.
5. Iniciar desenvolvimento das telas com design aprimorado.

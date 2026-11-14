# Nova DPS Informática - Sistema de Gestão & BI (v2.0)
> Projeto Integrador I - FATEC Ipiranga

Sistema moderno para gestão de ordens de serviço, assistência técnica e análise de dados gerenciais desenvolvido 100% em **Python (PySide6 + Fluent Design)** com persistência em **Banco de Dados Relacional**.

---

## 🚀 Funcionalidades
- **Interface Gráfica Windows 11 Fluent Design:** moderna, responsiva, com suporte a modo claro/escuro nativo.
- **Painel Executivo em Tempo Real:** métricas operacionais (total de chamados, faturamento, ticket médio, clientes ativos).
- **Fila de Serviços Operacional:** priorização automática por tempo de espera de atendimento.
- **Controle Completo (CRUD):** Clientes, Pedidos, Serviços, Peças e Pagamentos.
- **Rastreabilidade de Componentes:** peças alocadas por serviço e controle de custo vs. margem de venda.
- **Exportação Estrela para Power BI:** scripts que geram arquivos CSV prontos com dimensões e fatos para o dashboard acadêmico.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.11+
- **Interface Gráfica:** PySide6 + PySide6-Fluent-Widgets
- **Banco de Dados:** PostgreSQL / SQLite via SQLAlchemy 2.0
- **Análise de Dados:** Pandas + Power BI Desktop
- **Geração de Dados Sintéticos:** Faker (pt_BR)

---

## 💻 Como Rodar o Projeto

1. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Inicialize e popule o banco (com mais de 100 registros reais de teste):**
   ```powershell
   python scripts/popular_banco.py
   ```

3. **Inicie o aplicativo:**
   ```powershell
   python main.py
   ```

4. **(Opcional) Exportar dados para o Power BI:**
   ```powershell
   python scripts/exportar_powerbi.py
   ```
   *Os arquivos estarão em `docs/06_bi_powerbi/` prontos para abrir no Power BI.*

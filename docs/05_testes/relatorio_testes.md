# Relatório de Resultados de Testes de Software
## Projeto Integrador I - Nova DPS Informática

**Data de Execução:** 14/11/2026  
**Ferramenta Utilizada:** `pytest 8.4.0` com `Python 3.13`  
**Ambiente:** Windows 11 (x64) · SGBD Relacional (SQLAlchemy / SQLite & PostgreSQL)  

---

## 1. Resumo Executivo da Execução

| Métrica | Resultado |
|---|---|
| **Total de Testes Executados** | 6 |
| **Testes Aprovados (Passed)** | 6 (100%) |
| **Falhas ou Erros** | 0 |
| **Tempo Total de Execução** | ~0.75 segundos |
| **Status da Suíte** | ✅ **APROVADO (GREEN)** |

---

## 2. Detalhamento dos Casos de Teste Automatizados

### `TC-01: test_conexao_banco`
- **Objetivo:** Verificar se a engine do SQLAlchemy consegue estabelecer conexão ativa e responder à consulta canônica `SELECT 1`.
- **Resultado:** `PASSED` (Conexão estável e sem latência anormal).

### `TC-02: test_existencia_tabelas`
- **Objetivo:** Garantir a integridade física do esquema relacional conferindo a criação das 6 tabelas obrigatórias (`cliente`, `pedido`, `servico`, `orcamento`, `peca`, `pagamento`).
- **Resultado:** `PASSED` (Todas as 6 tabelas existem com suas respectivas chaves e índices).

### `TC-03: test_volume_minimo_tabela_principal`
- **Objetivo:** Validar o critério eliminatório do Prof. Antonio Guardado (Banco de Dados I): tabela principal com no mínimo 100 linhas.
- **Resultado:** `PASSED` (A tabela `pedido` possui 130 registros persistidos).

### `TC-04: test_calculo_kpis`
- **Objetivo:** Testar se o serviço de BI e métricas calcula corretamente o total de chamados ativos, faturamento bruto, ticket médio e clientes ativos sem gerar exceções de divisão por zero ou nulos.
- **Resultado:** `PASSED` (Valores monetários e contagens íntegros).

### `TC-05: test_fila_servicos_pendentes`
- **Objetivo:** Validar a extração operacional da fila de chamados técnicos ordenados por tempo de espera (excluindo os já concluídos/entregues).
- **Resultado:** `PASSED` (Registros retornados com dados completos do cliente e modelo).

### `TC-06: test_insercao_e_exclusao_logica_cliente`
- **Objetivo:** Validar a persistência do CRUD de clientes com dados completos de localização (bairro, endereço, cidade) e a manutenção da integridade de exclusão lógica (`ativo = 1`).
- **Resultado:** `PASSED` (Cliente persistido e recuperado com sucesso).

---

## 3. Evidência de Saída do Console

```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.0, pluggy-1.5.0
rootdir: C:\Users\aldiv\OneDrive\Desktop\codar\PROJETOS\PI-Faculdade
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.7.0, Faker-40.54.0
collected 6 items

tests\test_sistema.py ......                                             [100%]

============================== 6 passed in 0.75s ==============================
```

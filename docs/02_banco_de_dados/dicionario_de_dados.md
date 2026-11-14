# Dicionário de Dados - Nova DPS Informática
## Banco de Dados Relacional (SGBD: PostgreSQL / SQLite)

Este documento especifica a estrutura lógica e física de todas as tabelas do sistema, seus atributos, tipos primitivos, restrições de integridade e descrições semânticas.

---

### 1. Tabela: `cliente`
Armazena os dados cadastrais das pessoas físicas ou jurídicas proprietárias dos equipamentos.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_cliente` | INTEGER / SERIAL | Não | PK | Identificador único e sequencial do cliente |
| `nome` | VARCHAR(120) | Não | - | Nome completo ou Razão Social |
| `cpf_cnpj` | VARCHAR(18) | Sim | UK | CPF ou CNPJ único do cliente |
| `telefone` | VARCHAR(20) | Não | - | Número de telefone/WhatsApp de contato |
| `email` | VARCHAR(100) | Sim | - | Endereço eletrônico para envio de orçamentos |
| `endereco` | VARCHAR(200) | Sim | - | Logradouro e número |
| `bairro` | VARCHAR(60) | Sim | - | Bairro para análise demográfica e logística |
| `cidade` | VARCHAR(60) | Sim | - | Município (Padrão: 'São Paulo') |
| `uf` | VARCHAR(2) | Sim | - | Estado federativo (Padrão: 'SP') |
| `data_cadastro` | TIMESTAMP | Não | - | Data e hora do registro no sistema |
| `ativo` | BOOLEAN | Não | - | Indicador de exclusão lógica (1=Ativo, 0=Inativo) |

---

### 2. Tabela: `pedido` (Chamados / Ordens de Serviço)
Registra a entrada física de equipamentos na assistência técnica e a abertura do chamado.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_pedido` | INTEGER / SERIAL | Não | PK | Código identificador da Ordem de Serviço |
| `id_cliente` | INTEGER | Não | FK | Referência ao cliente solicitante (`cliente.id_cliente`) |
| `tipo_equipamento` | VARCHAR(50) | Não | - | Ex: Notebook, Desktop, Servidor, Placa-Mãe |
| `modelo_equipamento`| VARCHAR(100) | Não | - | Marca e modelo (ex: Dell Inspiron 15) |
| `numero_serie` | VARCHAR(60) | Sim | - | Número de série para controle patrimonial |
| `descricao_falha` | TEXT | Não | - | Relato do defeito fornecido pelo cliente |
| `acessorios_inclusos`| VARCHAR(200) | Sim | - | Acessórios deixados (carregador, cabos, etc.) |
| `data_abertura` | TIMESTAMP | Não | - | Data e hora da entrada na assistência |
| `status_pedido` | VARCHAR(30) | Não | - | Status: 'Aberto', 'Em Análise', 'Em Manutenção', 'Concluído', 'Entregue', 'Cancelado' |

---

### 3. Tabela: `servico` (Mão de Obra e Diagnóstico)
Detalha a execução técnica, atribuição de técnicos e mão de obra de reparo.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_servico` | INTEGER / SERIAL | Não | PK | Identificador da intervenção técnica |
| `id_pedido` | INTEGER | Não | FK | Referência à OS (`pedido.id_pedido`) |
| `tecnico_responsavel`| VARCHAR(100) | Não | - | Nome do técnico de bancada alocado |
| `tipo_reparo` | VARCHAR(80) | Não | - | Procedimento realizado (Reballing BGA, Troca de Tela, etc.) |
| `diagnostico_tecnico`| TEXT | Sim | - | Laudo técnico detalhado do defeito encontrado |
| `data_inicio` | TIMESTAMP | Sim | - | Início dos procedimentos em bancada |
| `data_conclusao` | TIMESTAMP | Sim | - | Finalização dos testes de bancada |
| `valor_mao_de_obra` | NUMERIC(10,2) | Não | - | Valor cobrado pela mão de obra técnica |
| `status_servico` | VARCHAR(30) | Não | - | 'Pendente', 'Em Andamento', 'Aguardando Peça', 'Finalizado', 'Cancelado' |

---

### 4. Tabela: `orcamento`
Gerencia a precificação formal, valores estimados vs finais e aprovação do cliente.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_orcamento` | INTEGER / SERIAL | Não | PK | Código do orçamento gerado |
| `id_pedido` | INTEGER | Não | FK | Referência à OS (`pedido.id_pedido`) |
| `valor_estimado` | NUMERIC(10,2) | Não | - | Estimativa inicial pré-diagnóstico |
| `valor_final` | NUMERIC(10,2) | Sim | - | Valor consolidado (peças + mão de obra) |
| `data_orcamento` | TIMESTAMP | Não | - | Data da elaboração do orçamento |
| `data_aprovacao` | TIMESTAMP | Sim | - | Data da autorização pelo cliente |
| `aprovado` | BOOLEAN | Não | - | 1 se aprovado pelo cliente, 0 se rejeitado/pendente |
| `observacoes` | TEXT | Sim | - | Condições comerciais, garantia e prazo |

---

### 5. Tabela: `peca` (Estoque e Rastreabilidade)
Controla os componentes eletrônicos utilizados em cada reparo e a margem de lucro.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_peca` | INTEGER / SERIAL | Não | PK | Código único do componente |
| `id_servico` | INTEGER | Sim | FK | Serviço onde foi instalada (`servico.id_servico`) |
| `codigo_referencia` | VARCHAR(50) | Sim | UK | Código SKU/part number do fabricante |
| `nome_peca` | VARCHAR(120) | Não | - | Descrição do componente (ex: CI de Charge, SSD NVMe 1TB) |
| `fornecedor` | VARCHAR(100) | Não | - | Empresa fornecedora da peça |
| `quantidade` | INTEGER | Não | - | Quantidade movimentada (padrão 1) |
| `custo_unitario` | NUMERIC(10,2) | Não | - | Valor de aquisição da peça |
| `preco_venda` | NUMERIC(10,2) | Não | - | Valor repassado na cobrança ao cliente |
| `data_entrada` | DATE | Não | - | Data de compra/entrada no estoque |

---

### 6. Tabela: `pagamento`
Registra as liquidações financeiras e quitação de ordens de serviço.

| Atributo | Tipo de Dado | Nulo? | Chave | Descrição / Regra |
|---|---|---|---|---|
| `id_pagamento` | INTEGER / SERIAL | Não | PK | Identificador da transação financeira |
| `id_pedido` | INTEGER | Não | FK | Referência à OS quitada (`pedido.id_pedido`) |
| `valor_pago` | NUMERIC(10,2) | Não | - | Montante recebido |
| `forma_pagamento` | VARCHAR(30) | Não | - | 'PIX', 'Cartão Crédito', 'Cartão Débito', 'Dinheiro', 'Boleto' |
| `data_pagamento` | TIMESTAMP | Não | - | Momento da confirmação do pagamento |
| `numero_parcelas` | INTEGER | Não | - | Número de parcelas (para cartão) |
| `status_pagamento` | VARCHAR(20) | Não | - | 'Confirmado', 'Pendente', 'Estornado' |

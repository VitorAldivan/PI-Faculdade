# Guia de Importação e Medidas DAX - Power BI Desktop
## Projeto Integrador I - Nova DPS Informática

Os dados exportados em formato **Esquema Estrela** estão localizados nesta pasta (`docs/06_bi_powerbi/`).

### Arquivos Gerados:
1. `dim_cliente.csv` (Dimensão Clientes)
2. `dim_pedido.csv` (Dimensão Pedidos / Ordens de Serviço)
3. `fato_servico.csv` (Fato Serviços / Mão de Obra)
4. `fato_pagamento.csv` (Fato Pagamentos e Fluxo Financeiro)
5. `fato_peca.csv` (Fato Peças e Componentes Utilizados)

---

### Relacionamentos no Power BI:
- `dim_cliente[id_cliente]` **1 -> N** `dim_pedido[id_cliente]`
- `dim_pedido[id_pedido]` **1 -> N** `fato_servico[id_pedido]`
- `dim_pedido[id_pedido]` **1 -> N** `fato_pagamento[id_pedido]`
- `fato_servico[id_servico]` **1 -> N** `fato_peca[id_servico]`

---

### Medidas DAX Prontas (Obrigatórias no Projeto):

```dax
Total Faturado = SUM(fato_pagamento[valor_pago])

Total Chamados = COUNTROWS(dim_pedido)

Ticket Medio = DIVIDE([Total Faturado], [Total Chamados], 0)

Total Mao de Obra = SUM(fato_servico[valor_mao_de_obra])

Custo Total Pecas = SUM(fato_peca[custo_unitario])

Lucro Estimado Pecas = SUMX(fato_peca, fato_peca[preco_venda] - fato_peca[custo_unitario])
```

---

### Visuais Recomendados no Dashboard:
1. **Cartões:** Total Faturado, Total de Chamados, Ticket Médio.
2. **Gráfico de Colunas:** Faturamento por Mês (`fato_pagamento[data_pagamento]`).
3. **Gráfico de Setor (Rosca):** Distribuição por Tipo de Reparo ou Forma de Pagamento.
4. **Tabela / Matriz:** Fila de serviços pendentes e tempo de espera.
5. **Segmentação de Dados (Filtros):** Status do Pedido, Bairro do Cliente, Técnico Responsável.

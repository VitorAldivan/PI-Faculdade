-- ==============================================================================
-- PROJETO INTEGRADOR I - FATEC IPIRANGA
-- CONSULTAS SQL OPERACIONAIS, ANALÍTICAS E GERENCIAIS (DISCIPLINA BANCO DE DADOS I)
-- ==============================================================================

-- 1. CONSULTA OPERACIONAL: FILA DE SERVIÇOS PENDENTES ORDENADA POR ESPERA
-- Pergunta de negócio: Quais chamados estão aguardando manutenção e há quanto tempo?
SELECT 
    p.id_pedido,
    c.nome AS cliente,
    c.telefone,
    p.modelo_equipamento,
    s.tipo_reparo,
    s.status_servico,
    p.data_abertura,
    ROUND(EXTRACT(EPOCH FROM (NOW() - p.data_abertura))/3600, 1) AS horas_espera
FROM pedido p
INNER JOIN cliente c ON p.id_cliente = c.id_cliente
LEFT JOIN servico s ON p.id_pedido = s.id_pedido
WHERE p.status_pedido NOT IN ('Entregue', 'Cancelado')
ORDER BY p.data_abertura ASC;

-- 2. CONSULTA ANALÍTICA/FINANCEIRA: BALANÇO POR PEDIDO (VALOR COBRADO vs PAGO)
-- Pergunta de negócio: Quais pedidos possuem pagamentos pendentes ou já estão quitados?
SELECT 
    p.id_pedido,
    c.nome AS cliente,
    p.modelo_equipamento,
    COALESCE(o.valor_final, o.valor_estimado, 0.00) AS valor_orcado,
    COALESCE(SUM(pg.valor_pago), 0.00) AS total_pago,
    (COALESCE(o.valor_final, o.valor_estimado, 0.00) - COALESCE(SUM(pg.valor_pago), 0.00)) AS saldo_devedor
FROM pedido p
INNER JOIN cliente c ON p.id_cliente = c.id_cliente
LEFT JOIN orcamento o ON p.id_pedido = o.id_pedido
LEFT JOIN pagamento pg ON p.id_pedido = pg.id_pedido
GROUP BY p.id_pedido, c.nome, p.modelo_equipamento, o.valor_final, o.valor_estimado
ORDER BY saldo_devedor DESC;

-- 3. CONSULTA GERENCIAL: RASTREABILIDADE DE PEÇAS UTILIZADAS POR EQUIPAMENTO
-- Pergunta de negócio: Quais peças e custos foram alocados em cada ordem de serviço?
SELECT 
    p.id_pedido,
    p.modelo_equipamento,
    s.tecnico_responsavel,
    pc.codigo_referencia,
    pc.nome_peca,
    pc.fornecedor,
    pc.custo_unitario,
    pc.preco_venda,
    (pc.preco_venda - pc.custo_unitario) AS margem_lucro
FROM peca pc
INNER JOIN servico s ON pc.id_servico = s.id_servico
INNER JOIN pedido p ON s.id_pedido = p.id_pedido
ORDER BY p.id_pedido DESC;

-- 4. CONSULTA ANALÍTICA COM FUNÇÃO DE JANELA (WINDOW FUNCTION):
-- Pergunta de negócio: Ranking e média móvel do faturamento mensal
SELECT 
    TO_CHAR(data_pagamento, 'YYYY-MM') AS mes_ano,
    forma_pagamento,
    SUM(valor_pago) AS faturamento_forma,
    SUM(SUM(valor_pago)) OVER (PARTITION BY TO_CHAR(data_pagamento, 'YYYY-MM')) AS faturamento_total_mes,
    RANK() OVER (PARTITION BY TO_CHAR(data_pagamento, 'YYYY-MM') ORDER BY SUM(valor_pago) DESC) AS rank_preferencia
FROM pagamento
WHERE status_pagamento = 'Confirmado'
GROUP BY TO_CHAR(data_pagamento, 'YYYY-MM'), forma_pagamento
ORDER BY mes_ano DESC, rank_preferencia;

from sqlalchemy import text
from src.nova_dps.infra.database import engine

class DashboardService:
    @staticmethod
    def obter_kpis():
        with engine.connect() as conn:
            total_pedidos = conn.execute(text("SELECT COUNT(*) FROM pedido")).scalar() or 0
            pedidos_abertos = conn.execute(text("SELECT COUNT(*) FROM pedido WHERE status_pedido IN ('Aberto', 'Em Análise', 'Em Manutenção')")).scalar() or 0
            faturamento_total = conn.execute(text("SELECT SUM(valor_pago) FROM pagamento WHERE status_pagamento = 'Confirmado'")).scalar() or 0.0
            ticket_medio = conn.execute(text("SELECT AVG(valor_pago) FROM pagamento WHERE status_pagamento = 'Confirmado'")).scalar() or 0.0
            total_clientes = conn.execute(text("SELECT COUNT(*) FROM cliente WHERE ativo = 1")).scalar() or 0
            
            return {
                "total_pedidos": total_pedidos,
                "pedidos_abertos": pedidos_abertos,
                "faturamento_total": float(faturamento_total),
                "ticket_medio": float(ticket_medio),
                "total_clientes": total_clientes
            }

    @staticmethod
    def fila_servicos_pendentes():
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    p.id_pedido,
                    c.nome AS cliente,
                    c.telefone,
                    p.modelo_equipamento,
                    s.tipo_reparo,
                    s.status_servico,
                    p.data_abertura
                FROM pedido p
                INNER JOIN cliente c ON p.id_cliente = c.id_cliente
                LEFT JOIN servico s ON p.id_pedido = s.id_pedido
                WHERE p.status_pedido NOT IN ('Entregue', 'Cancelado')
                ORDER BY p.data_abertura ASC
                LIMIT 50
            """)
            return conn.execute(query).mappings().fetchall()

    @staticmethod
    def balanco_financeiro():
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    p.id_pedido,
                    c.nome AS cliente,
                    p.modelo_equipamento,
                    COALESCE(o.valor_final, o.valor_estimado, 0.0) AS valor_orcado,
                    COALESCE(SUM(pg.valor_pago), 0.0) AS total_pago,
                    (COALESCE(o.valor_final, o.valor_estimado, 0.0) - COALESCE(SUM(pg.valor_pago), 0.0)) AS saldo_devedor
                FROM pedido p
                INNER JOIN cliente c ON p.id_cliente = c.id_cliente
                LEFT JOIN orcamento o ON p.id_pedido = o.id_pedido
                LEFT JOIN pagamento pg ON p.id_pedido = pg.id_pedido
                GROUP BY p.id_pedido, c.nome, p.modelo_equipamento, o.valor_final, o.valor_estimado
                ORDER BY saldo_devedor DESC
                LIMIT 50
            """)
            return conn.execute(query).mappings().fetchall()

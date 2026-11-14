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
    def faturamento_por_mes():
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    strftime('%Y-%m', data_pagamento) AS mes,
                    SUM(valor_pago) AS total
                FROM pagamento
                WHERE status_pagamento = 'Confirmado'
                GROUP BY strftime('%Y-%m', data_pagamento)
                ORDER BY mes ASC
                LIMIT 6
            """)
            return conn.execute(query).fetchall()

    @staticmethod
    def distribuicao_tipos_reparo():
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    tipo_reparo,
                    COUNT(*) as qtd
                FROM servico
                GROUP BY tipo_reparo
                ORDER BY qtd DESC
                LIMIT 5
            """)
            return conn.execute(query).fetchall()

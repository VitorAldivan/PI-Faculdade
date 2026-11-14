from sqlalchemy import text
from src.nova_dps.infra.database import engine

class CrudService:
    @staticmethod
    def listar_clientes():
        with engine.connect() as conn:
            return conn.execute(text("SELECT id_cliente, nome, cpf_cnpj, telefone, email, bairro, cidade FROM cliente WHERE ativo = 1 ORDER BY id_cliente DESC")).mappings().fetchall()

    @staticmethod
    def salvar_cliente(nome, cpf_cnpj, telefone, email, endereco, bairro, cidade="São Paulo"):
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO cliente (nome, cpf_cnpj, telefone, email, endereco, bairro, cidade)
                VALUES (:nome, :cpf, :tel, :email, :end, :bairro, :cidade)
            """), {"nome": nome, "cpf": cpf_cnpj, "tel": telefone, "email": email, "end": endereco, "bairro": bairro, "cidade": cidade})

    @staticmethod
    def atualizar_cliente(id_cliente, nome, cpf_cnpj, telefone, email, endereco, bairro, cidade):
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE cliente 
                SET nome = :nome, cpf_cnpj = :cpf, telefone = :tel, email = :email, 
                    endereco = :end, bairro = :bairro, cidade = :cidade
                WHERE id_cliente = :id
            """), {
                "nome": nome, "cpf": cpf_cnpj, "tel": telefone, "email": email,
                "end": endereco, "bairro": bairro, "cidade": cidade, "id": id_cliente
            })

    @staticmethod
    def inativar_cliente(id_cliente):
        with engine.begin() as conn:
            conn.execute(text("UPDATE cliente SET ativo = 0 WHERE id_cliente = :id"), {"id": id_cliente})

    @staticmethod
    def atualizar_status_pedido(id_pedido, novo_status):
        with engine.begin() as conn:
            conn.execute(text("UPDATE pedido SET status_pedido = :st WHERE id_pedido = :id"), {"st": novo_status, "id": id_pedido})

    @staticmethod
    def atualizar_status_servico(id_servico, novo_status):
        with engine.begin() as conn:
            conn.execute(text("UPDATE servico SET status_servico = :st WHERE id_servico = :id"), {"st": novo_status, "id": id_servico})

    @staticmethod
    def listar_pedidos():
        with engine.connect() as conn:
            return conn.execute(text("""
                SELECT p.id_pedido, c.nome AS cliente, p.tipo_equipamento, p.modelo_equipamento, p.status_pedido, p.data_abertura
                FROM pedido p
                INNER JOIN cliente c ON p.id_cliente = c.id_cliente
                ORDER BY p.id_pedido DESC
            """)).mappings().fetchall()

    @staticmethod
    def salvar_pedido(id_cliente, tipo_eq, modelo, falha, status_p):
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO pedido (id_cliente, tipo_equipamento, modelo_equipamento, descricao_falha, status_pedido)
                VALUES (:idc, :tipo, :mod, :falha, :st)
            """), {"idc": id_cliente, "tipo": tipo_eq, "mod": modelo, "falha": falha, "st": status_p})

    @staticmethod
    def listar_servicos():
        with engine.connect() as conn:
            return conn.execute(text("""
                SELECT s.id_servico, s.id_pedido, p.modelo_equipamento, s.tecnico_responsavel, s.tipo_reparo, s.valor_mao_de_obra, s.status_servico
                FROM servico s
                INNER JOIN pedido p ON s.id_pedido = p.id_pedido
                ORDER BY s.id_servico DESC
            """)).mappings().fetchall()

    @staticmethod
    def listar_pecas():
        with engine.connect() as conn:
            return conn.execute(text("""
                SELECT id_peca, id_servico, codigo_referencia, nome_peca, fornecedor, quantidade, custo_unitario, preco_venda
                FROM peca
                ORDER BY id_peca DESC
            """)).mappings().fetchall()

    @staticmethod
    def listar_pagamentos():
        with engine.connect() as conn:
            return conn.execute(text("""
                SELECT pg.id_pagamento, pg.id_pedido, c.nome AS cliente, pg.valor_pago, pg.forma_pagamento, pg.data_pagamento, pg.status_pagamento
                FROM pagamento pg
                INNER JOIN pedido p ON pg.id_pedido = p.id_pedido
                INNER JOIN cliente c ON p.id_cliente = c.id_cliente
                ORDER BY pg.id_pagamento DESC
            """)).mappings().fetchall()

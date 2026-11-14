import os
import pandas as pd
from sqlalchemy import text
from src.nova_dps.infra.database import engine

def exportar_para_powerbi(output_dir="docs/06_bi_powerbi"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Exportando dados em formato estrela para {output_dir}...")

    with engine.connect() as conn:
        # Dimensões
        df_clientes = pd.read_sql("SELECT id_cliente, nome, telefone, email, bairro, cidade, uf FROM cliente", conn)
        df_clientes.to_csv(os.path.join(output_dir, "dim_cliente.csv"), index=False, encoding="utf-8")

        df_pedidos = pd.read_sql("SELECT id_pedido, id_cliente, tipo_equipamento, modelo_equipamento, status_pedido, data_abertura FROM pedido", conn)
        df_pedidos.to_csv(os.path.join(output_dir, "dim_pedido.csv"), index=False, encoding="utf-8")

        # Fatos
        df_servicos = pd.read_sql("SELECT id_servico, id_pedido, tecnico_responsavel, tipo_reparo, valor_mao_de_obra, status_servico FROM servico", conn)
        df_servicos.to_csv(os.path.join(output_dir, "fato_servico.csv"), index=False, encoding="utf-8")

        df_pagamentos = pd.read_sql("SELECT id_pagamento, id_pedido, valor_pago, forma_pagamento, data_pagamento, status_pagamento FROM pagamento", conn)
        df_pagamentos.to_csv(os.path.join(output_dir, "fato_pagamento.csv"), index=False, encoding="utf-8")

        df_pecas = pd.read_sql("SELECT id_peca, id_servico, codigo_referencia, nome_peca, fornecedor, quantidade, custo_unitario, preco_venda FROM peca", conn)
        df_pecas.to_csv(os.path.join(output_dir, "fato_peca.csv"), index=False, encoding="utf-8")

    print("Exportação concluída com sucesso! Arquivos CSV prontos para importação no Power BI Desktop.")

if __name__ == "__main__":
    exportar_para_powerbi()

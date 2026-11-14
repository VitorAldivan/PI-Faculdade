import os
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///nova_dps.db")
engine = create_engine(DATABASE_URL)
fake = Faker('pt_BR')

def inicializar_e_popular(qtd_pedidos=120):
    print("Iniciando criação das tabelas e carga sintética de dados (100+ registros)...")
    
    with engine.begin() as conn:
        # Criação compatível
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(120) NOT NULL,
            cpf_cnpj VARCHAR(18) UNIQUE,
            telefone VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            endereco VARCHAR(200),
            bairro VARCHAR(60),
            cidade VARCHAR(60) DEFAULT 'São Paulo',
            uf VARCHAR(2) DEFAULT 'SP',
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1
        );
        """))
        
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pedido (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            tipo_equipamento VARCHAR(50) NOT NULL,
            modelo_equipamento VARCHAR(100) NOT NULL,
            numero_serie VARCHAR(60),
            descricao_falha TEXT NOT NULL,
            acessorios_inclusos VARCHAR(200),
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status_pedido VARCHAR(30) DEFAULT 'Aberto',
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS servico (
            id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            tecnico_responsavel VARCHAR(100) NOT NULL,
            tipo_reparo VARCHAR(80) NOT NULL,
            diagnostico_tecnico TEXT,
            data_inicio TIMESTAMP,
            data_conclusao TIMESTAMP,
            valor_mao_de_obra NUMERIC(10, 2) DEFAULT 0.00,
            status_servico VARCHAR(30) DEFAULT 'Pendente',
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS orcamento (
            id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            valor_estimado NUMERIC(10, 2) NOT NULL,
            valor_final NUMERIC(10, 2),
            data_orcamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_aprovacao TIMESTAMP,
            aprovado BOOLEAN DEFAULT 0,
            observacoes TEXT,
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS peca (
            id_peca INTEGER PRIMARY KEY AUTOINCREMENT,
            id_servico INTEGER,
            codigo_referencia VARCHAR(50) UNIQUE,
            nome_peca VARCHAR(120) NOT NULL,
            fornecedor VARCHAR(100) NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 1,
            custo_unitario NUMERIC(10, 2) NOT NULL,
            preco_venda NUMERIC(10, 2) NOT NULL,
            data_entrada DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (id_servico) REFERENCES servico(id_servico)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pagamento (
            id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            valor_pago NUMERIC(10, 2) NOT NULL,
            forma_pagamento VARCHAR(30) NOT NULL,
            data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            numero_parcelas INTEGER DEFAULT 1,
            status_pagamento VARCHAR(20) DEFAULT 'Confirmado',
            FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        );
        """))

        # Checar se já existem dados
        qtd_atual = conn.execute(text("SELECT COUNT(*) FROM pedido")).scalar()
        if qtd_atual and qtd_atual >= qtd_pedidos:
            print(f"O banco já possui {qtd_atual} pedidos cadastrados.")
            return

        print("Gerando clientes...")
        bairros_sp = ['Ipiranga', 'Sacomã', 'Cursino', 'Vila Mariana', 'Mooca', 'Tatuapé', 'Jabaquara', 'Bela Vista', 'Saúde', 'Pinheiros']
        tecnicos = ['Carlos Eduardo', 'Jonny Araujo', 'Matheus Ferrari', 'Wellingtton Lima', 'Luiz Enrique']
        equipamentos = [
            ('Notebook', ['Dell Inspiron 15', 'Lenovo ThinkPad E14', 'Acer Aspire 5', 'MacBook Air M1', 'HP Pavilion 14', 'Asus VivoBook 15']),
            ('Desktop', ['PC Gamer Ryzen 5 5600', 'Workstation Intel i7 12700', 'PC Escritório Core i3', 'PC Gamer RTX 4060']),
            ('Placa-Mãe', ['ASUS TUF B550M', 'Gigabyte B450M DS3H', 'MSI MAG B650', 'ASRock Steel Legend']),
            ('Servidor', ['Dell PowerEdge R440', 'HP ProLiant DL380', 'Lenovo ThinkSystem SR650'])
        ]
        falhas = [
            'Não liga e superaquece na região do conector DC Jack',
            'Curto-circuito na linha de 19V principal',
            'Artefatos na tela e desligamento intermitente após 10 minutos de uso',
            'Sem vídeo após atualização de BIOS',
            'Tela trincada após queda e conector flat danificado',
            'Teclado falhando teclas após derramamento acidental de líquido',
            'Lentidão extrema, sistema não inicializa no SSD NVMe',
            'Bateria estufada e não segura carga fora da tomada'
        ]
        reparos = [
            ('Troca de CI de Charge e reparo de trilha', 280.00),
            ('Reballing de chipset BGA e troca de pasta térmica', 450.00),
            ('Troca de tela LED IPS 15.6 polegadas', 180.00),
            ('Gravação de BIOS com programadora Eprom', 150.00),
            ('Banho químico ultrassônico para desoxidação de placa', 220.00),
            ('Troca de conector DC Jack', 120.00),
            ('Substituição de cooler e limpeza preventiva', 90.00),
            ('Formatação com backup e reinstalação de drivers', 120.00)
        ]
        fornecedores = ['Distribuidora Paulista de Eletrônicos', 'TechParts Brasil', 'Sampa Chips & BGA', 'Global Componentes', 'Center Screen SP']

        # Inserir 60 clientes
        for i in range(60):
            conn.execute(text("""
                INSERT INTO cliente (nome, cpf_cnpj, telefone, email, endereco, bairro, cidade, uf)
                VALUES (:nome, :cpf, :tel, :email, :end, :bairro, 'São Paulo', 'SP')
            """), {
                "nome": fake.name(),
                "cpf": fake.cpf(),
                "tel": fake.phone_number(),
                "email": fake.email(),
                "end": fake.street_address(),
                "bairro": random.choice(bairros_sp)
            })

        # Buscar IDs dos clientes
        clientes_ids = [row[0] for row in conn.execute(text("SELECT id_cliente FROM cliente")).fetchall()]

        # Inserir 120+ pedidos com serviços, orçamentos e pagamentos
        data_base = datetime.now() - timedelta(days=180)

        for p_idx in range(qtd_pedidos):
            cliente_id = random.choice(clientes_ids)
            tipo_eq, modelos = random.choice(equipamentos)
            modelo = random.choice(modelos)
            falha = random.choice(falhas)
            data_abertura = data_base + timedelta(days=random.randint(1, 175), hours=random.randint(8, 17))
            status_p = random.choice(['Aberto', 'Em Análise', 'Em Manutenção', 'Concluído', 'Entregue', 'Entregue'])

            result_pedido = conn.execute(text("""
                INSERT INTO pedido (id_cliente, tipo_equipamento, modelo_equipamento, numero_serie, descricao_falha, data_abertura, status_pedido)
                VALUES (:idc, :tipo, :mod, :sn, :falha, :dt, :st)
            """), {
                "idc": cliente_id,
                "tipo": tipo_eq,
                "mod": modelo,
                "sn": f"SN-{fake.hexify(text='^^^^^^^^')}",
                "falha": falha,
                "dt": data_abertura,
                "st": status_p
            })
            pedido_id = result_pedido.lastrowid

            # Serviço associado
            reparo_nome, valor_mao_obra = random.choice(reparos)
            status_s = 'Finalizado' if status_p in ['Concluído', 'Entregue'] else ('Em Andamento' if status_p == 'Em Manutenção' else 'Pendente')
            data_inicio = data_abertura + timedelta(hours=random.randint(2, 24))
            data_conclusao = data_inicio + timedelta(days=random.randint(1, 4)) if status_s == 'Finalizado' else None

            result_servico = conn.execute(text("""
                INSERT INTO servico (id_pedido, tecnico_responsavel, tipo_reparo, diagnostico_tecnico, data_inicio, data_conclusao, valor_mao_de_obra, status_servico)
                VALUES (:idp, :tec, :tipo, :diag, :dti, :dtc, :vlr, :sts)
            """), {
                "idp": pedido_id,
                "tec": random.choice(tecnicos),
                "tipo": reparo_nome,
                "diag": f"Análise constatou necessidade de {reparo_nome.lower()}.",
                "dti": data_inicio,
                "dtc": data_conclusao,
                "vlr": valor_mao_obra,
                "sts": status_s
            })
            servico_id = result_servico.lastrowid

            # Peça usada (em 70% dos casos)
            custo_peca = 0.00
            preco_peca = 0.00
            if random.random() > 0.3:
                custo_peca = round(random.uniform(40.0, 350.0), 2)
                preco_peca = round(custo_peca * random.uniform(1.4, 2.0), 2)
                conn.execute(text("""
                    INSERT INTO peca (id_servico, codigo_referencia, nome_peca, fornecedor, quantidade, custo_unitario, preco_venda)
                    VALUES (:ids, :cod, :nome, :forn, :qtd, :custo, :preco)
                """), {
                    "ids": servico_id,
                    "cod": f"PEC-{fake.unique.random_number(digits=6)}",
                    "nome": f"Componente Reparo {tipo_eq}",
                    "forn": random.choice(fornecedores),
                    "qtd": 1,
                    "custo": custo_peca,
                    "preco": preco_peca
                })

            # Orçamento
            valor_total = round(valor_mao_obra + preco_peca, 2)
            aprovado = status_p not in ['Aberto', 'Cancelado']
            conn.execute(text("""
                INSERT INTO orcamento (id_pedido, valor_estimado, valor_final, data_orcamento, data_aprovacao, aprovado, observacoes)
                VALUES (:idp, :ve, :vf, :dto, :dta, :apv, 'Orçamento aprovado pelo cliente via WhatsApp.')
            """), {
                "idp": pedido_id,
                "ve": round(valor_total * 1.1, 2),
                "vf": valor_total,
                "dto": data_abertura + timedelta(hours=3),
                "dta": data_abertura + timedelta(hours=6) if aprovado else None,
                "apv": 1 if aprovado else 0
            })

            # Pagamento (se entregue ou concluído)
            if status_p in ['Concluído', 'Entregue']:
                forma = random.choice(['PIX', 'Cartão Crédito', 'Cartão Débito', 'Dinheiro'])
                dt_pagamento = (data_conclusao or data_abertura) + timedelta(hours=random.randint(1, 12))
                conn.execute(text("""
                    INSERT INTO pagamento (id_pedido, valor_pago, forma_pagamento, data_pagamento, status_pagamento)
                    VALUES (:idp, :vlr, :forma, :dt, 'Confirmado')
                """), {
                    "idp": pedido_id,
                    "vlr": valor_total,
                    "forma": forma,
                    "dt": dt_pagamento
                })

    print(f"Sucesso! Banco populado com 60 clientes e {qtd_pedidos} pedidos com rastreabilidade completa.")

if __name__ == "__main__":
    inicializar_e_popular(130)

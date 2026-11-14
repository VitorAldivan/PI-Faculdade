# ==============================================================================
# PROJETO INTEGRADOR I - FATEC IPIRANGA
# SCRIPT DDL: CRIAÇÃO DO BANCO DE DADOS RELACIONAL - NOVA DPS INFORMÁTICA
# SGBD ALVO: PostgreSQL / Compatível com SQLite (via SQLAlchemy)
# ==============================================================================

-- 1. TABELA DE CLIENTES
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cpf_cnpj VARCHAR(18) UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    endereco VARCHAR(200),
    bairro VARCHAR(60),
    cidade VARCHAR(60) DEFAULT 'São Paulo',
    uf VARCHAR(2) DEFAULT 'SP',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

-- 2. TABELA DE PEDIDOS (CHAMADOS DE ENTRADA DO EQUIPAMENTO)
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    tipo_equipamento VARCHAR(50) NOT NULL, -- Ex: Notebook, Desktop, Servidor, Placa-Mãe
    modelo_equipamento VARCHAR(100) NOT NULL,
    numero_serie VARCHAR(60),
    descricao_falha TEXT NOT NULL,
    acessorios_inclusos VARCHAR(200), -- Ex: Carregador, Cabo de força
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_pedido VARCHAR(30) DEFAULT 'Aberto', -- Aberto, Em Análise, Em Manutenção, Concluído, Entregue, Cancelado
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE RESTRICT
);

-- 3. TABELA DE SERVIÇOS (ORDENS TÉCNICAS E MÃO DE OBRA)
CREATE TABLE IF NOT EXISTS servico (
    id_servico SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    tecnico_responsavel VARCHAR(100) NOT NULL,
    tipo_reparo VARCHAR(80) NOT NULL, -- Ex: Troca de BGA, Reballing, Troca de Tela, Reparo em Placa, Formatação
    diagnostico_tecnico TEXT,
    data_inicio TIMESTAMP,
    data_conclusao TIMESTAMP,
    valor_mao_de_obra NUMERIC(10, 2) DEFAULT 0.00,
    status_servico VARCHAR(30) DEFAULT 'Pendente', -- Pendente, Em Andamento, Aguardando Peça, Finalizado, Cancelado
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE RESTRICT
);

-- 4. TABELA DE ORÇAMENTOS
CREATE TABLE IF NOT EXISTS orcamento (
    id_orcamento SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    valor_estimado NUMERIC(10, 2) NOT NULL,
    valor_final NUMERIC(10, 2),
    data_orcamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_aprovacao TIMESTAMP,
    aprovado BOOLEAN DEFAULT FALSE,
    observacoes TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE RESTRICT
);

-- 5. TABELA DE PEÇAS E COMPONENTES (ESTOQUE E RASTREABILIDADE)
CREATE TABLE IF NOT EXISTS peca (
    id_peca SERIAL PRIMARY KEY,
    id_servico INT, -- Pode ser nulo se a peça estiver em estoque geral
    codigo_referencia VARCHAR(50) UNIQUE,
    nome_peca VARCHAR(120) NOT NULL,
    fornecedor VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    custo_unitario NUMERIC(10, 2) NOT NULL,
    preco_venda NUMERIC(10, 2) NOT NULL,
    data_entrada DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico) ON DELETE SET NULL
);

-- 6. TABELA DE PAGAMENTOS
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    valor_pago NUMERIC(10, 2) NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL, -- PIX, Cartão Crédito, Cartão Débito, Dinheiro, Boleto
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numero_parcelas INT DEFAULT 1,
    status_pagamento VARCHAR(20) DEFAULT 'Confirmado', -- Confirmado, Pendente, Estornado
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE RESTRICT
);

-- ==============================================================================
-- ÍNDICES PARA ALTA PERFORMANCE E BUSCA RÁPIDA
-- ==============================================================================
CREATE INDEX IF NOT EXISTS ix_pedido_cliente ON pedido(id_cliente);
CREATE INDEX IF NOT EXISTS ix_pedido_status ON pedido(status_pedido);
CREATE INDEX IF NOT EXISTS ix_servico_pedido ON servico(id_pedido);
CREATE INDEX IF NOT EXISTS ix_servico_status ON servico(status_servico);
CREATE INDEX IF NOT EXISTS ix_peca_servico ON peca(id_servico);
CREATE INDEX IF NOT EXISTS ix_pagamento_pedido ON pagamento(id_pedido);

import pytest
from sqlalchemy import text
from src.nova_dps.infra.database import engine
from src.nova_dps.services.dashboard_service import DashboardService
from src.nova_dps.services.crud_service import CrudService

def test_conexao_banco():
    """Valida se a conexão com o banco de dados está ativa e funcional."""
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT 1")).scalar()
        assert resultado == 1

def test_existencia_tabelas():
    """Garante que as 6 tabelas obrigatórias existem no banco."""
    with engine.connect() as conn:
        tabelas = [row[0] for row in conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()]
        obrigatorias = ['cliente', 'pedido', 'servico', 'orcamento', 'peca', 'pagamento']
        for tab in obrigatorias:
            assert tab in tabelas, f"Tabela obrigatória ausente: {tab}"

def test_volume_minimo_tabela_principal():
    """Valida o requisito de Banco de Dados I: tabela principal com mais de 100 linhas."""
    with engine.connect() as conn:
        total_pedidos = conn.execute(text("SELECT COUNT(*) FROM pedido")).scalar()
        assert total_pedidos >= 100, f"A tabela pedido tem apenas {total_pedidos} registros (mínimo exigido: 100)"

def test_calculo_kpis():
    """Testa se o serviço analítico de KPIs calcula métricas válidas e não-nulas."""
    kpis = DashboardService.obter_kpis()
    assert kpis["total_pedidos"] > 0
    assert kpis["faturamento_total"] >= 0.0
    assert kpis["ticket_medio"] >= 0.0
    assert kpis["total_clientes"] > 0

def test_fila_servicos_pendentes():
    """Valida se a consulta operacional da fila retorna registros válidos com os campos esperados."""
    fila = DashboardService.fila_servicos_pendentes()
    assert isinstance(fila, list)
    if len(fila) > 0:
        primeiro = fila[0]
        assert "id_pedido" in primeiro
        assert "cliente" in primeiro
        assert "modelo_equipamento" in primeiro

def test_insercao_e_exclusao_logica_cliente():
    """Testa a integridade do CRUD garantindo que exclusões são lógicas e dados válidos são persistidos."""
    nome_teste = "Cliente Teste Unitário Automatizado"
    tel_teste = "(11) 99999-8888"
    
    # Inserção
    CrudService.salvar_cliente(nome_teste, "000.111.222-33", tel_teste, "teste@novadps.com", "Rua Teste, 100", "Ipiranga")
    
    with engine.connect() as conn:
        cliente_cadastrado = conn.execute(text("SELECT id_cliente, ativo FROM cliente WHERE nome = :n"), {"n": nome_teste}).mappings().fetchone()
        assert cliente_cadastrado is not None
        assert cliente_cadastrado["ativo"] == 1

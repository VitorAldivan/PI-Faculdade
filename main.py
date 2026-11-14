import sys
import os

# Garantir PYTHONPATH no diretório raiz
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from qfluentwidgets import (
    FluentWindow, NavigationInterface, NavigationItemPosition,
    FluentIcon as FIF, setTheme, Theme
)

from src.nova_dps.ui.paginas.dashboard_page import DashboardPage
from src.nova_dps.ui.paginas.clientes_page import ClientesPage
from src.nova_dps.ui.paginas.pedidos_page import PedidosPage
from src.nova_dps.ui.paginas.servicos_page import ServicosPage
from src.nova_dps.ui.paginas.pecas_page import PecasPage
from src.nova_dps.ui.paginas.pagamentos_page import PagamentosPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova DPS Informática - Sistema de Gestão & BI v2.0")
        self.resize(1280, 800)

        # Iniciar páginas
        self.dashboard_page = DashboardPage(self)
        self.clientes_page = ClientesPage(self)
        self.pedidos_page = PedidosPage(self)
        self.servicos_page = ServicosPage(self)
        self.pecas_page = PecasPage(self)
        self.pagamentos_page = PagamentosPage(self)

        self.init_navigation()

    def init_navigation(self):
        # Adicionar itens de navegação lateral com ícones Fluent
        self.addSubInterface(self.dashboard_page, FIF.SPEED_HIGH, "Painel & Indicadores")
        self.addSubInterface(self.pedidos_page, FIF.TILES, "Ordens de Serviço")
        self.addSubInterface(self.clientes_page, FIF.PEOPLE, "Clientes")
        self.addSubInterface(self.servicos_page, FIF.DEVELOPER_TOOLS, "Serviços Técnicos")
        self.addSubInterface(self.pecas_page, FIF.APPLICATION, "Peças & Estoque")
        self.addSubInterface(self.pagamentos_page, FIF.SHOPPING_CART, "Financeiro")

        # Configurar tema moderno
        setTheme(Theme.AUTO)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

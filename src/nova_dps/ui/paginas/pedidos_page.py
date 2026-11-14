from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem
from qfluentwidgets import (
    TableWidget, PrimaryPushButton, FluentIcon as FIF, TitleLabel, CaptionLabel
)
from src.nova_dps.services.crud_service import CrudService

class PedidosPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PedidosPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        title = TitleLabel("Ordens de Serviço e Chamados (Pedidos)", self)
        subtitle = CaptionLabel("Controle de fluxo técnico desde a entrada do equipamento", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID Pedido", "Cliente", "Tipo", "Modelo", "Status", "Data Entrada"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_pedidos()

    def carregar_pedidos(self):
        pedidos = CrudService.listar_pedidos()
        self.tabela.setRowCount(len(pedidos))
        for row_idx, p in enumerate(pedidos):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{p['id_pedido']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(str(p['cliente'])))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(p['tipo_equipamento'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(p['modelo_equipamento'])))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(p['status_pedido'])))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(p['data_abertura'])[:16]))

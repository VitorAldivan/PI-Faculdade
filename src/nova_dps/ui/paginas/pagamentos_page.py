from PySide6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import TableWidget, TitleLabel, CaptionLabel
from src.nova_dps.services.crud_service import CrudService

class PagamentosPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PagamentosPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        title = TitleLabel("Financeiro & Faturamento", self)
        subtitle = CaptionLabel("Controle de quitações, formas de pagamento e fluxo de caixa", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID Pagamento (Fixo)", "ID OS (Fixo)", "Cliente", "Valor Pago", "Forma Pagamento", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_dados()

    def carregar_dados(self):
        pagamentos = CrudService.listar_pagamentos()
        self.tabela.setRowCount(len(pagamentos))
        for row_idx, pg in enumerate(pagamentos):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{pg['id_pagamento']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(f"#{pg['id_pedido']}"))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(pg['cliente'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(f"R$ {float(pg['valor_pago']):,.2f}"))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(pg['forma_pagamento'])))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(pg['status_pagamento'])))

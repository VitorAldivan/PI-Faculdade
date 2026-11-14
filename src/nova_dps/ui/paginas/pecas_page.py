from PySide6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import TableWidget, TitleLabel, CaptionLabel
from src.nova_dps.services.crud_service import CrudService

class PecasPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PecasPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        title = TitleLabel("Estoque & Rastreabilidade de Peças", self)
        subtitle = CaptionLabel("Controle de componentes, fornecedores e margem de revenda", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID Peça (Fixo)", "Código SKU", "Componente / Peça", "Fornecedor", "Qtd", "Custo", "Venda"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_dados()

    def carregar_dados(self):
        pecas = CrudService.listar_pecas()
        self.tabela.setRowCount(len(pecas))
        for row_idx, p in enumerate(pecas):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{p['id_peca']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(str(p['codigo_referencia'] or '-')))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(p['nome_peca'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(p['fornecedor'])))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(p['quantidade'])))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(f"R$ {float(p['custo_unitario']):,.2f}"))
            self.tabela.setItem(row_idx, 6, QTableWidgetItem(f"R$ {float(p['preco_venda']):,.2f}"))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QScrollArea
from qfluentwidgets import (
    CardWidget, TableWidget, PrimaryPushButton, PushButton,
    FluentIcon as FIF, TitleLabel, SubtitleLabel, CaptionLabel, InfoBar, InfoBarPosition
)
from src.nova_dps.services.dashboard_service import DashboardService

class DashboardPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("DashboardPage")
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.container = QWidget()
        self.setWidget(self.container)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        # Cabeçalho
        title = TitleLabel("Painel Executivo & Indicadores", self.container)
        subtitle = CaptionLabel("Visão operacional e financeira em tempo real da assistência técnica (Visualizações gráficas centralizadas no Power BI)", self.container)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Linha de KPIs
        self.kpis_layout = QHBoxLayout()
        self.kpis_layout.setSpacing(16)
        layout.addLayout(self.kpis_layout)

        # Fila de Serviços
        sec_title = SubtitleLabel("Fila de Serviços Pendentes (Ordenada por tempo de espera)", self.container)
        layout.addWidget(sec_title)

        self.tabela = TableWidget(self.container)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setWordWrap(False)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID Pedido", "Cliente", "Telefone", "Equipamento", "Reparo", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setMinimumHeight(380)
        layout.addWidget(self.tabela)

        # Barra de Ações (Atualizar, Gerar Relatório PDF e Exportar para Power BI)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.btn_bi = PushButton(FIF.PIE_SINGLE, "Atualizar Dataset Power BI (CSV)", self.container)
        self.btn_bi.clicked.connect(self.exportar_bi)
        
        self.btn_pdf = PushButton(FIF.DOCUMENT, "Exportar Relatório Executivo (PDF)", self.container)
        self.btn_pdf.clicked.connect(self.exportar_pdf)
        
        self.btn_refresh = PrimaryPushButton(FIF.SYNC, "Atualizar Indicadores", self.container)
        self.btn_refresh.clicked.connect(self.carregar_dados)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_bi)
        btn_layout.addWidget(self.btn_pdf)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        self.carregar_dados()

    def exportar_bi(self):
        from scripts.exportar_powerbi import exportar_para_powerbi
        try:
            exportar_para_powerbi()
            InfoBar.success(
                title="Power BI Atualizado!",
                content="Os arquivos CSV do esquema estrela foram atualizados em docs/06_bi_powerbi/.",
                orient=InfoBarPosition.TOP,
                duration=3500,
                parent=self.container
            )
        except Exception as e:
            InfoBar.error(title="Erro ao exportar", content=str(e), orient=InfoBarPosition.TOP, parent=self.container)

    def exportar_pdf(self):
        from src.nova_dps.services.relatorio_service import RelatorioPdfService
        import os
        caminho = RelatorioPdfService.gerar_relatorio_gerencial()
        InfoBar.success(
            title="Relatório Gerado com Sucesso!",
            content=f"Arquivo PDF salvo em: {os.path.basename(caminho)}",
            orient=InfoBarPosition.TOP,
            isClosable=True,
            duration=3500,
            parent=self.container
        )

    def carregar_dados(self):
        kpis = DashboardService.obter_kpis()

        # Limpar cards anteriores
        while self.kpis_layout.count():
            item = self.kpis_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Adicionar cards modernos
        cards_data = [
            ("Chamados Ativos", str(kpis["pedidos_abertos"]), FIF.ACCEPT_MEDIUM),
            ("Total de Pedidos", str(kpis["total_pedidos"]), FIF.HISTORY),
            ("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), FIF.TAG),
            ("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), FIF.PIE_SINGLE),
            ("Clientes Cadastrados", str(kpis["total_clientes"]), FIF.PEOPLE),
        ]

        for rotulo, valor, icone in cards_data:
            card = CardWidget(self.container)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(16, 14, 16, 14)
            lbl_rotulo = CaptionLabel(rotulo, card)
            lbl_valor = TitleLabel(valor, card)
            lbl_valor.setStyleSheet("color: #0078D4; font-weight: bold;")
            c_layout.addWidget(lbl_rotulo)
            c_layout.addWidget(lbl_valor)
            self.kpis_layout.addWidget(card)

        # Carregar tabela da fila
        fila = DashboardService.fila_servicos_pendentes()
        self.tabela.setRowCount(len(fila))
        for row_idx, item in enumerate(fila):
            from PySide6.QtWidgets import QTableWidgetItem
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{item['id_pedido']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(str(item['cliente'])))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(item['telefone'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(item['modelo_equipamento'])))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(item['tipo_reparo'] or 'Em triagem')))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(item['status_servico'] or 'Aberto')))

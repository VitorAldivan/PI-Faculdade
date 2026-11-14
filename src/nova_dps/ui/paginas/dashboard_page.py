from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QHeaderView, QScrollArea
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries
from qfluentwidgets import (
    CardWidget, TableWidget, PrimaryPushButton, PushButton,
    FluentIcon as FIF, TitleLabel, SubtitleLabel, CaptionLabel
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
        subtitle = CaptionLabel("Visão operacional e financeira em tempo real da assistência técnica", self.container)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Linha de KPIs
        self.kpis_layout = QHBoxLayout()
        self.kpis_layout.setSpacing(16)
        layout.addLayout(self.kpis_layout)

        # Linha de Gráficos Nativos
        self.graficos_layout = QHBoxLayout()
        self.graficos_layout.setSpacing(16)

        # Card Gráfico de Colunas (Faturamento Mensal)
        self.card_barras = CardWidget(self.container)
        barras_vbox = QVBoxLayout(self.card_barras)
        barras_vbox.setContentsMargins(16, 12, 16, 12)
        lbl_barras = SubtitleLabel("Faturamento por Mês (R$)", self.card_barras)
        barras_vbox.addWidget(lbl_barras)
        self.chart_view_barras = QChartView(self.card_barras)
        self.chart_view_barras.setRenderHint(QPainter.Antialiasing)
        self.chart_view_barras.setMinimumHeight(240)
        barras_vbox.addWidget(self.chart_view_barras)
        self.graficos_layout.addWidget(self.card_barras, 3)

        # Card Gráfico de Rosca (Distribuição de Reparos)
        self.card_rosca = CardWidget(self.container)
        rosca_vbox = QVBoxLayout(self.card_rosca)
        rosca_vbox.setContentsMargins(16, 12, 16, 12)
        lbl_rosca = SubtitleLabel("Top Reparos Técnicos", self.card_rosca)
        rosca_vbox.addWidget(lbl_rosca)
        self.chart_view_rosca = QChartView(self.card_rosca)
        self.chart_view_rosca.setRenderHint(QPainter.Antialiasing)
        self.chart_view_rosca.setMinimumHeight(240)
        rosca_vbox.addWidget(self.chart_view_rosca)
        self.graficos_layout.addWidget(self.card_rosca, 2)

        layout.addLayout(self.graficos_layout)

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
        self.tabela.setMinimumHeight(220)
        layout.addWidget(self.tabela)

        # Botão Atualizar e Gerar Relatório PDF
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_pdf = PushButton(FIF.DOCUMENT, "Exportar Relatório Executivo (PDF)", self.container)
        self.btn_pdf.clicked.connect(self.exportar_pdf)
        
        self.btn_refresh = PrimaryPushButton(FIF.SYNC, "Atualizar Indicadores", self.container)
        self.btn_refresh.clicked.connect(self.carregar_dados)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_pdf)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        self.carregar_dados()

    def exportar_pdf(self):
        from src.nova_dps.services.relatorio_service import RelatorioPdfService
        from qfluentwidgets import InfoBar, InfoBarPosition
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

        # Adicionar novos cards modernos
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

        # Montar Gráfico de Colunas (Faturamento)
        dados_meses = DashboardService.faturamento_por_mes()
        chart_barras = QChart()
        chart_barras.setAnimationOptions(QChart.SeriesAnimations)
        chart_barras.legend().setVisible(False)

        bar_set = QBarSet("Faturamento")
        bar_set.setColor("#0078D4")
        categorias = []
        max_val = 1000.0

        for mes, total in dados_meses:
            categorias.append(str(mes)[5:]) # MM
            val = float(total or 0)
            bar_set.append(val)
            if val > max_val:
                max_val = val

        series_bar = QBarSeries()
        series_bar.append(bar_set)
        chart_barras.addSeries(series_bar)

        axis_x = QBarCategoryAxis()
        axis_x.append(categorias if categorias else ["Meses"])
        chart_barras.addAxis(axis_x, Qt.AlignBottom)
        series_bar.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max_val * 1.15)
        chart_barras.addAxis(axis_y, Qt.AlignLeft)
        series_bar.attachAxis(axis_y)

        self.chart_view_barras.setChart(chart_barras)

        # Montar Gráfico de Rosca (Reparos)
        dados_reparos = DashboardService.distribuicao_tipos_reparo()
        chart_rosca = QChart()
        chart_rosca.setAnimationOptions(QChart.SeriesAnimations)
        chart_rosca.legend().setVisible(True)
        chart_rosca.legend().setAlignment(Qt.AlignRight)

        pie_series = QPieSeries()
        pie_series.setHoleSize(0.38)

        for reparo, qtd in dados_reparos:
            pie_series.append(str(reparo)[:18], int(qtd))

        chart_rosca.addSeries(pie_series)
        self.chart_view_rosca.setChart(chart_rosca)

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

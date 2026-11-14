from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import (
    TableWidget, PrimaryPushButton, LineEdit, ComboBox,
    FluentIcon as FIF, TitleLabel, CaptionLabel, InfoBar, InfoBarPosition
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

        # Formulário Rápido de Abertura de Ordem de Serviço
        form_row = QHBoxLayout()
        form_row.setSpacing(10)

        self.cb_clientes = ComboBox(self)
        self.cb_clientes.setPlaceholderText("Selecione o Cliente")

        self.cb_tipo = ComboBox(self)
        self.cb_tipo.addItems(["Notebook", "Desktop", "Placa-Mãe", "Servidor", "Monitor"])

        self.txt_modelo = LineEdit(self)
        self.txt_modelo.setPlaceholderText("Marca e Modelo (ex: Dell G15)")

        self.txt_falha = LineEdit(self)
        self.txt_falha.setPlaceholderText("Defeito Relatado")

        self.btn_salvar = PrimaryPushButton(FIF.ADD, "Abrir Nova OS", self)
        self.btn_salvar.clicked.connect(self.salvar_pedido)

        form_row.addWidget(self.cb_clientes, 2)
        form_row.addWidget(self.cb_tipo, 1)
        form_row.addWidget(self.txt_modelo, 2)
        form_row.addWidget(self.txt_falha, 2)
        form_row.addWidget(self.btn_salvar, 1)
        layout.addLayout(form_row)

        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers) # IDs e dados inalteráveis manualmente
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID OS (Fixo)", "Cliente", "Tipo", "Modelo", "Status", "Data Entrada"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_clientes_combo()
        self.carregar_pedidos()

    def carregar_clientes_combo(self):
        self.cb_clientes.clear()
        clientes = CrudService.listar_clientes()
        self.clientes_map = {}
        for c in clientes:
            texto = f"#{c['id_cliente']} - {c['nome']}"
            self.cb_clientes.addItem(texto)
            self.clientes_map[texto] = c['id_cliente']

    def salvar_pedido(self):
        cliente_txt = self.cb_clientes.currentText()
        tipo = self.cb_tipo.currentText()
        modelo = self.txt_modelo.text().strip()
        falha = self.txt_falha.text().strip()

        if cliente_txt and modelo and falha:
            id_cliente = self.clientes_map.get(cliente_txt)
            if id_cliente:
                CrudService.salvar_pedido(id_cliente, tipo, modelo, falha, "Aberto")
                self.txt_modelo.clear()
                self.txt_falha.clear()
                self.carregar_pedidos()
                InfoBar.success(
                    title="Ordem de Serviço Aberta!",
                    content=f"Equipamento {modelo} registrado com sucesso para {cliente_txt}!",
                    orient=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )

    def carregar_pedidos(self):
        pedidos = CrudService.listar_pedidos()
        self.tabela.setRowCount(len(pedidos))
        for row_idx, p in enumerate(pedidos):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{p['id_pedido']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(str(p['cliente'])))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(p['tipo_equipamento'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(p['modelo_equipamento'])))
            
            # ComboBox Interativo com as 3 opções solicitadas
            cb_status = ComboBox(self)
            cb_status.addItems(["Pendente", "Em Andamento", "Finalizado"])
            
            status_banco = str(p['status_pedido'])
            # Normalizar status para as 3 opções
            if status_banco in ["Concluído", "Entregue", "Finalizado"]:
                cb_status.setCurrentText("Finalizado")
            elif status_banco in ["Em Andamento", "Em Manutenção", "Em Análise"]:
                cb_status.setCurrentText("Em Andamento")
            else:
                cb_status.setCurrentText("Pendente")

            # Conectar alteração imediata no banco
            cb_status.currentTextChanged.connect(
                lambda novo_st, id_p=p['id_pedido']: self.on_status_changed(id_p, novo_st)
            )
            self.tabela.setCellWidget(row_idx, 4, cb_status)

            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(p['data_abertura'])[:16]))

    def on_status_changed(self, id_pedido, novo_status):
        CrudService.atualizar_status_pedido(id_pedido, novo_status)
        InfoBar.success(
            title="Status Atualizado",
            content=f"OS #{id_pedido} atualizada para: {novo_status}",
            orient=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

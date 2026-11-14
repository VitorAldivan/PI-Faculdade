from PySide6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import TableWidget, TitleLabel, CaptionLabel, ComboBox, InfoBar, InfoBarPosition
from src.nova_dps.services.crud_service import CrudService

class ServicosPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ServicosPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        title = TitleLabel("Gestão de Serviços e Reparos Técnicos", self)
        subtitle = CaptionLabel("Controle de mão de obra técnica, diagnóstico e execução de reparo", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID Serviço (Fixo)", "ID OS (Fixo)", "Equipamento", "Técnico", "Tipo de Reparo", "Mão de Obra", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_dados()

    def carregar_dados(self):
        servicos = CrudService.listar_servicos()
        self.tabela.setRowCount(len(servicos))
        for row_idx, s in enumerate(servicos):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{s['id_servico']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(f"#{s['id_pedido']}"))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(s['modelo_equipamento'])))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(s['tecnico_responsavel'])))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(s['tipo_reparo'])))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(f"R$ {float(s['valor_mao_de_obra']):,.2f}"))
            
            # ComboBox Interativo com 3 opções
            cb_status = ComboBox(self)
            cb_status.addItems(["Pendente", "Em Andamento", "Finalizado"])
            
            st_banco = str(s['status_servico'])
            if st_banco in ["Finalizado", "Concluído"]:
                cb_status.setCurrentText("Finalizado")
            elif st_banco in ["Em Andamento"]:
                cb_status.setCurrentText("Em Andamento")
            else:
                cb_status.setCurrentText("Pendente")

            cb_status.currentTextChanged.connect(
                lambda novo_st, id_s=s['id_servico']: self.on_status_changed(id_s, novo_st)
            )
            self.tabela.setCellWidget(row_idx, 6, cb_status)

    def on_status_changed(self, id_servico, novo_status):
        CrudService.atualizar_status_servico(id_servico, novo_status)
        InfoBar.success(
            title="Status de Serviço Atualizado",
            content=f"Serviço #{id_servico} alterado para: {novo_status}",
            orient=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem
from qfluentwidgets import (
    TableWidget, PrimaryPushButton, PushButton, LineEdit,
    FluentIcon as FIF, TitleLabel, SubtitleLabel, CaptionLabel
)
from src.nova_dps.services.crud_service import CrudService

class ClientesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ClientesPage")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(20)

        title = TitleLabel("Cadastro e Gestão de Clientes", self)
        subtitle = CaptionLabel("Controle centralizado de clientes e contatos", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Barra de Formulário Rápido
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)
        self.txt_nome = LineEdit(self)
        self.txt_nome.setPlaceholderText("Nome Completo")
        self.txt_tel = LineEdit(self)
        self.txt_tel.setPlaceholderText("Telefone/WhatsApp")
        self.txt_email = LineEdit(self)
        self.txt_email.setPlaceholderText("E-mail")
        self.btn_salvar = PrimaryPushButton(FIF.ADD, "Novo Cliente", self)
        self.btn_salvar.clicked.connect(self.salvar_cliente)

        form_layout.addWidget(self.txt_nome)
        form_layout.addWidget(self.txt_tel)
        form_layout.addWidget(self.txt_email)
        form_layout.addWidget(self.btn_salvar)
        layout.addLayout(form_layout)

        # Tabela
        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF/CNPJ", "Telefone", "E-mail", "Bairro"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_clientes()

    def salvar_cliente(self):
        nome = self.txt_nome.text().strip()
        tel = self.txt_tel.text().strip()
        email = self.txt_email.text().strip()
        if nome and tel:
            CrudService.salvar_cliente(nome, "", tel, email, "", "Ipiranga")
            self.txt_nome.clear()
            self.txt_tel.clear()
            self.txt_email.clear()
            self.carregar_clientes()

    def carregar_clientes(self):
        clientes = CrudService.listar_clientes()
        self.tabela.setRowCount(len(clientes))
        for row_idx, c in enumerate(clientes):
            self.tabela.setItem(row_idx, 0, QTableWidgetItem(f"#{c['id_cliente']}"))
            self.tabela.setItem(row_idx, 1, QTableWidgetItem(str(c['nome'])))
            self.tabela.setItem(row_idx, 2, QTableWidgetItem(str(c['cpf_cnpj'] or '-')))
            self.tabela.setItem(row_idx, 3, QTableWidgetItem(str(c['telefone'])))
            self.tabela.setItem(row_idx, 4, QTableWidgetItem(str(c['email'] or '-')))
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(c['bairro'] or 'São Paulo')))

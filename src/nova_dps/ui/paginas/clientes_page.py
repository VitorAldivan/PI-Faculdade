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

        # Barra de Formulário Rápido com Localização Completa
        form_row1 = QHBoxLayout()
        form_row1.setSpacing(10)
        self.txt_nome = LineEdit(self)
        self.txt_nome.setPlaceholderText("Nome Completo / Razão Social")
        self.txt_cpf = LineEdit(self)
        self.txt_cpf.setPlaceholderText("CPF ou CNPJ")
        self.txt_tel = LineEdit(self)
        self.txt_tel.setPlaceholderText("Telefone / WhatsApp")
        self.txt_email = LineEdit(self)
        self.txt_email.setPlaceholderText("E-mail")

        form_row1.addWidget(self.txt_nome, 2)
        form_row1.addWidget(self.txt_cpf, 1)
        form_row1.addWidget(self.txt_tel, 1)
        form_row1.addWidget(self.txt_email, 2)
        layout.addLayout(form_row1)

        form_row2 = QHBoxLayout()
        form_row2.setSpacing(10)
        self.txt_endereco = LineEdit(self)
        self.txt_endereco.setPlaceholderText("Endereço (Rua, Av, Número, Complemento)")
        self.txt_bairro = LineEdit(self)
        self.txt_bairro.setPlaceholderText("Bairro (Ex: Ipiranga, Mooca, Sacomã)")
        self.txt_cidade = LineEdit(self)
        self.txt_cidade.setPlaceholderText("Cidade (Padrão: São Paulo)")
        self.btn_salvar = PrimaryPushButton(FIF.ADD, "Cadastrar Cliente", self)
        self.btn_salvar.clicked.connect(self.salvar_cliente)

        form_row2.addWidget(self.txt_endereco, 2)
        form_row2.addWidget(self.txt_bairro, 1)
        form_row2.addWidget(self.txt_cidade, 1)
        form_row2.addWidget(self.btn_salvar, 1)
        layout.addLayout(form_row2)

        # Tabela
        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF/CNPJ", "Telefone", "E-mail", "Bairro", "Cidade"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)

        self.carregar_clientes()

    def salvar_cliente(self):
        nome = self.txt_nome.text().strip()
        cpf = self.txt_cpf.text().strip()
        tel = self.txt_tel.text().strip()
        email = self.txt_email.text().strip()
        endereco = self.txt_endereco.text().strip()
        bairro = self.txt_bairro.text().strip()
        cidade = self.txt_cidade.text().strip() or "São Paulo"
        
        if nome and tel:
            CrudService.salvar_cliente(nome, cpf, tel, email, endereco, bairro)
            self.txt_nome.clear()
            self.txt_cpf.clear()
            self.txt_tel.clear()
            self.txt_email.clear()
            self.txt_endereco.clear()
            self.txt_bairro.clear()
            self.txt_cidade.clear()
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
            self.tabela.setItem(row_idx, 5, QTableWidgetItem(str(c['bairro'] or '-')))
            self.tabela.setItem(row_idx, 6, QTableWidgetItem(str(c['cidade'] or 'São Paulo')))

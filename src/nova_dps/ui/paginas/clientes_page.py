from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem, QAbstractItemView
from qfluentwidgets import (
    TableWidget, PrimaryPushButton, PushButton, LineEdit,
    FluentIcon as FIF, TitleLabel, SubtitleLabel, CaptionLabel, InfoBar, InfoBarPosition
)
from src.nova_dps.services.crud_service import CrudService
from src.nova_dps.services.validadores import validar_cpf, validar_telefone, validar_email

class ClientesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("ClientesPage")
        self.id_em_edicao = None # None = modo novo; int = modo edição
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 24, 36, 24)
        layout.setSpacing(16)

        title = TitleLabel("Cadastro e Gestão de Clientes", self)
        subtitle = CaptionLabel("Controle centralizado com cadastro, edição de dados e histórico", self)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Indicador de modo (Novo vs Edição)
        self.lbl_modo = CaptionLabel("Modo: Novo Cadastro de Cliente (Clique 2x na tabela para editar)", self)
        self.lbl_modo.setStyleSheet("color: #0078D4; font-weight: bold;")
        layout.addWidget(self.lbl_modo)

        # Linha 1 de Campos
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

        # Linha 2 de Campos + Botões de Ação
        form_row2 = QHBoxLayout()
        form_row2.setSpacing(10)
        self.txt_endereco = LineEdit(self)
        self.txt_endereco.setPlaceholderText("Endereço (Rua, Av, Número, Complemento)")
        self.txt_bairro = LineEdit(self)
        self.txt_bairro.setPlaceholderText("Bairro (Ex: Ipiranga, Mooca, Sacomã)")
        self.txt_cidade = LineEdit(self)
        self.txt_cidade.setPlaceholderText("Cidade (Padrão: São Paulo)")

        self.btn_salvar = PrimaryPushButton(FIF.SAVE, "Salvar Cliente", self)
        self.btn_salvar.clicked.connect(self.salvar_cliente)

        self.btn_cancelar = PushButton(FIF.CANCEL, "Cancelar", self)
        self.btn_cancelar.clicked.connect(self.limpar_formulario)
        self.btn_cancelar.setVisible(False)

        form_row2.addWidget(self.txt_endereco, 2)
        form_row2.addWidget(self.txt_bairro, 1)
        form_row2.addWidget(self.txt_cidade, 1)
        form_row2.addWidget(self.btn_salvar, 1)
        form_row2.addWidget(self.btn_cancelar, 1)
        layout.addLayout(form_row2)

        # Tabela
        self.tabela = TableWidget(self)
        self.tabela.setBorderVisible(True)
        self.tabela.setBorderRadius(8)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["ID (Fixo)", "Nome", "CPF/CNPJ", "Telefone", "E-mail", "Bairro", "Cidade"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.itemDoubleClicked.connect(self.ao_dar_duplo_clique)
        layout.addWidget(self.tabela)

        self.carregar_clientes()

    def ao_dar_duplo_clique(self, item):
        row = item.row()
        id_str = self.tabela.item(row, 0).text().replace("#", "")
        self.id_em_edicao = int(id_str)

        # Puxar dados da linha selecionada para os campos
        self.txt_nome.setText(self.tabela.item(row, 1).text())
        cpf_txt = self.tabela.item(row, 2).text()
        self.txt_cpf.setText(cpf_txt if cpf_txt != '-' else "")
        self.txt_tel.setText(self.tabela.item(row, 3).text())
        email_txt = self.tabela.item(row, 4).text()
        self.txt_email.setText(email_txt if email_txt != '-' else "")
        bairro_txt = self.tabela.item(row, 5).text()
        self.txt_bairro.setText(bairro_txt if bairro_txt != '-' else "")
        self.txt_cidade.setText(self.tabela.item(row, 6).text())

        # Atualizar estado visual para MODO EDIÇÃO
        self.lbl_modo.setText(f"Modo: Editando Cliente #{self.id_em_edicao} ({self.txt_nome.text()})")
        self.lbl_modo.setStyleSheet("color: #D83B01; font-weight: bold;")
        self.btn_salvar.setText("Atualizar Dados")
        self.btn_salvar.setIcon(FIF.UPDATE)
        self.btn_cancelar.setVisible(True)

    def limpar_formulario(self):
        self.id_em_edicao = None
        self.txt_nome.clear()
        self.txt_cpf.clear()
        self.txt_tel.clear()
        self.txt_email.clear()
        self.txt_endereco.clear()
        self.txt_bairro.clear()
        self.txt_cidade.clear()
        self.lbl_modo.setText("Modo: Novo Cadastro de Cliente (Clique 2x na tabela para editar)")
        self.lbl_modo.setStyleSheet("color: #0078D4; font-weight: bold;")
        self.btn_salvar.setText("Salvar Cliente")
        self.btn_salvar.setIcon(FIF.SAVE)
        self.btn_cancelar.setVisible(False)

    def salvar_cliente(self):
        nome = self.txt_nome.text().strip()
        cpf = self.txt_cpf.text().strip()
        tel = self.txt_tel.text().strip()
        email = self.txt_email.text().strip()
        endereco = self.txt_endereco.text().strip()
        bairro = self.txt_bairro.text().strip()
        cidade = self.txt_cidade.text().strip() or "São Paulo"
        
        # Validações
        if not nome or len(nome) < 3:
            InfoBar.warning(title="Nome Inválido", content="Informe o nome completo (mínimo 3 letras).", orient=InfoBarPosition.TOP, parent=self)
            return
        if not tel or not validar_telefone(tel):
            InfoBar.warning(title="Telefone Inválido", content="Informe DDD + Número (10 ou 11 dígitos).", orient=InfoBarPosition.TOP, parent=self)
            return
        if cpf and not validar_cpf(cpf):
            InfoBar.warning(title="CPF Inválido", content="Dígitos verificadores do CPF inválidos.", orient=InfoBarPosition.TOP, parent=self)
            return
        if email and not validar_email(email):
            InfoBar.warning(title="E-mail Inválido", content="Formato de e-mail incorreto.", orient=InfoBarPosition.TOP, parent=self)
            return

        try:
            if self.id_em_edicao:
                # ATUALIZAÇÃO
                CrudService.atualizar_cliente(self.id_em_edicao, nome, cpf, tel, email, endereco, bairro, cidade)
                InfoBar.success(
                    title="Dados Atualizados com Sucesso!",
                    content=f"As informações do cliente #{self.id_em_edicao} foram salvas.",
                    orient=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            else:
                # NOVO CADASTRO
                CrudService.salvar_cliente(nome, cpf, tel, email, endereco, bairro, cidade)
                InfoBar.success(
                    title="Cliente Cadastrado!",
                    content=f"{nome} cadastrado com sucesso.",
                    orient=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
            
            self.limpar_formulario()
            self.carregar_clientes()
        except Exception as e:
            InfoBar.error(title="Erro ao Gravar", content=str(e), orient=InfoBarPosition.TOP, parent=self)

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

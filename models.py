import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox, QStackedWidget, QMainWindow, QComboBox
import os

arquivo_txt = 'pacientes.txt'

# Função para salvar os dados no arquivo de texto
def salvar_dados(nome, nascimento, sexo, carteira_sus):
    with open(arquivo_txt, 'a') as arquivo:
        arquivo.write(f"{nome},{nascimento},{sexo},{carteira_sus}\n")


# Função para carregar os dados do arquivo de texto
def carregar_dados():
    pacientes = []
    if os.path.exists(arquivo_txt):
        with open(arquivo_txt, 'r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                pacientes.append(linha.strip().split(','))
    return pacientes


class TelaPrincipal(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.setWindowTitle("Pacientes")

        # Layout principal
        layout_principal = QVBoxLayout()

        # Label com o texto grande
        self.label_titulo = QLabel("Pacientes")
        self.label_titulo.setStyleSheet("font-size: 24px;")
        layout_principal.addWidget(self.label_titulo)

        # Botões
        self.botao_atualizar = QPushButton("Atualizar Página")
        self.botao_atualizar.clicked.connect(self.atualizar_pagina)
        layout_principal.addWidget(self.botao_atualizar)

        self.botao_adicionar = QPushButton("Adicionar Paciente")
        self.botao_adicionar.clicked.connect(self.mudar_para_tela_adicionar)
        layout_principal.addWidget(self.botao_adicionar)

        # Tabela para mostrar os pacientes cadastrados
        self.tabela_pacientes = QTableWidget()
        self.tabela_pacientes.setColumnCount(4)
        self.tabela_pacientes.setHorizontalHeaderLabels(["Nome", "Nascimento", "Sexo", "Carteira SUS"])
        layout_principal.addWidget(self.tabela_pacientes)

        self.setLayout(layout_principal)
        self.listar_pacientes()


    def atualizar_pagina(self):
        self.listar_pacientes()


    def listar_pacientes(self):
        self.tabela_pacientes.setRowCount(0)
        pacientes = carregar_dados()
        for paciente in pacientes:
            row_position = self.tabela_pacientes.rowCount()
            self.tabela_pacientes.insertRow(row_position)
            self.tabela_pacientes.setItem(row_position, 0, QTableWidgetItem(paciente[0]))
            self.tabela_pacientes.setItem(row_position, 1, QTableWidgetItem(paciente[1]))
            self.tabela_pacientes.setItem(row_position, 2, QTableWidgetItem(paciente[2]))
            self.tabela_pacientes.setItem(row_position, 3, QTableWidgetItem(paciente[3]))

    def mudar_para_tela_adicionar(self):
        self.stacked_widget.setCurrentIndex(1)


class TelaCadastro(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.setWindowTitle("Adicionar Paciente")

        # Layout principal
        layout_principal = QVBoxLayout()

        # Layout para os campos de entrada
        layout_campos = QVBoxLayout()

        # Campo Nome
        self.label_nome = QLabel("Nome:")
        self.entry_nome = QLineEdit()
        layout_campos.addWidget(self.label_nome)
        layout_campos.addWidget(self.entry_nome)

        # Campo Data de Nascimento
        self.label_nascimento = QLabel("Data de Nascimento:")
        self.entry_nascimento = QLineEdit()
        layout_campos.addWidget(self.label_nascimento)
        layout_campos.addWidget(self.entry_nascimento)

        # Campo Sexo
        self.label_sexo = QLabel("Sexo:")
        self.entry_sexo = QComboBox()
        self.entry_sexo.addItems(["Feminino", "Masculino"])
        layout_campos.addWidget(self.label_sexo)
        layout_campos.addWidget(self.entry_sexo)

        # Campo Carteira do SUS
        self.label_carteira_sus = QLabel("Carteira do SUS:")
        self.entry_carteira_sus = QLineEdit()
        layout_campos.addWidget(self.label_carteira_sus)
        layout_campos.addWidget(self.entry_carteira_sus)

        layout_principal.addLayout(layout_campos)

        # Botão para adicionar paciente
        self.botao_adicionar = QPushButton("Adicionar Paciente")
        self.botao_adicionar.clicked.connect(self.adicionar_paciente)
        layout_principal.addWidget(self.botao_adicionar)

        # Botão para voltar à tela principal
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.clicked.connect(self.voltar_para_tela_principal)
        layout_principal.addWidget(self.botao_voltar)

        # Define o layout da janela
        self.setLayout(layout_principal)


    def adicionar_paciente(self):
        nome = self.entry_nome.text()
        nascimento = self.entry_nascimento.text()
        sexo = self.entry_sexo.text()
        carteira_sus = self.entry_carteira_sus.text()

        if nome and nascimento and sexo and carteira_sus:
            salvar_dados(nome, nascimento, sexo, carteira_sus)
            self.entry_nome.clear()
            self.entry_nascimento.clear()
            self.entry_sexo.clear()
            self.entry_carteira_sus.clear()
            
            QMessageBox.information(self, "Sucesso", "Paciente adicionado com sucesso.")
        else:
            QMessageBox.warning(self, "Campos vazios", "Por favor, preencha todos os campos.")

    def voltar_para_tela_principal(self):
        self.stacked_widget.setCurrentIndex(0)


# Classe para montrar tela principal e tela de cadastro
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Pacientes")
        self.setGeometry(50, 50, 425, 50)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.tela_principal = TelaPrincipal(self.stacked_widget)
        self.tela_cadastro = TelaCadastro(self.stacked_widget)

        self.stacked_widget.addWidget(self.tela_principal)
        self.stacked_widget.addWidget(self.tela_cadastro)

        self.stacked_widget.setCurrentIndex(0)


# Executa a aplicação
app = QApplication(sys.argv)
janela = MainWindow()
janela.show()
sys.exit(app.exec_())
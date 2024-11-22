import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, 
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QWidget, QMessageBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite/PyQt - Cadastro")
        self.setGeometry(100, 100, 600, 400)
        
        self.conn = sqlite3.connect("cadastro.db") #gera documentação db
        self.cursor = self.conn.cursor()
        self.create_table()

        self.layout = QVBoxLayout()

        self.name_label = QLabel("nome:")
        self.name_input = QLineEdit()
        self.age_label = QLabel("idade:")
        self.age_input = QLineEdit()

        self.add_button = QPushButton("adicionar Registro")
        self.add_button.clicked.connect(self.add_record)

        self.load_button = QPushButton("carregar Registros")
        self.load_button.clicked.connect(self.load_records)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["nome", "idade"])

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def create_table(self):
        """cria a tabela no banco de dados."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_record(self):
        """adc registro ao bd."""
        nome = self.name_input.text()
        idade = self.age_input.text()

        if nome and idade.isdigit():
            self.cursor.execute("INSERT INTO pessoas (nome, idade) VALUES (?, ?)", (nome, int(idade)))
            self.conn.commit()
            QMessageBox.information(self, "sucesso", "adicionado com sucesso!")
            self.name_input.clear()
            self.age_input.clear()
        else:
            QMessageBox.warning(self, "erro", "preencha todos os campos corretamente!")

    def load_records(self):
        """carrega os registros do banco de dados para a tabela."""
        self.cursor.execute("SELECT nome, idade FROM pessoas")
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

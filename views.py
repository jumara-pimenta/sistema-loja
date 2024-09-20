from PyQt5.QtCore import Qt
import re

import models
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QDialog, QTableWidget, QVBoxLayout, QPushButton, \
    QHeaderView, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QTableWidgetItem

from PyQt5.QtGui import QColor


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('HAVAN - Sistema de Vendas')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu('Arquivo')
        cruds_menu = menubar.addMenu('Cadastros')
        process_menu = menubar.addMenu('Processos')
        about_menu = menubar.addMenu('Sobre')

        # file_menu action
        action_exit = QAction('Sair', self)
        action_exit.triggered.connect(self.close)

        file_menu.addAction(action_exit)

        # cruds menu actions
        action_department = QAction('Departamento', self)
        action_department.triggered.connect(self.open_department_list)
        action_employee = QAction('Funcionário', self)
        action_employee.triggered.connect(self.open_employee_list)
        action_supplier = QAction('Fornecedor', self)
        action_supplier.triggered.connect(self.open_supplier_list)
        action_marital_status = QAction('Estado civil', self)
        action_branch = QAction('Filial', self)
        cruds_menu.addAction(action_department)
        cruds_menu.addAction(action_employee)
        cruds_menu.addAction(action_supplier)
        cruds_menu.addAction(action_marital_status)
        cruds_menu.addAction(action_branch)

        # about menu action
        action_info = QAction('Informações', self)
        action_info.triggered.connect(self.show_about_message)
        about_menu.addAction(action_info)

    def show_about_message(self):
        QMessageBox.about(self, "Sobre", "Sistema de vendas da Loja Havan")

    def open_department_list(self):
        form = DepartmentList(self)
        form.exec_()

    def open_employee_list(self):
        form = EmployeeList(self)
        form.exec_()

    def open_supplier_list(self):
        form = SupplierList(self)
        form.exec_()

class DepartmentList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Listagem dos Departamentos')
        self.resize(600, 400)

        # Styling for the buttons
        button_style = '''
            QPushButton {
                background-color: #4682B4; /* Steel Blue */
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A9BD4; /* Lighter Steel Blue */
            }
        '''

        # Button for "New Department"
        self.button_new = QPushButton('Novo', self)
        self.button_new.clicked.connect(self.open_department_item)
        self.button_new.setStyleSheet(button_style)
        self.button_new.setMinimumHeight(40)

        # Button for "Refresh"
        self.button_refresh = QPushButton('Atualizar dados', self)
        self.button_refresh.clicked.connect(self.populate_table)
        self.button_refresh.setStyleSheet(button_style)
        self.button_refresh.setMinimumHeight(40)

        # Styling for the table
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome'])
        header = self.table.horizontalHeader()
        header.setStyleSheet('background-color: #F0F8FF; color: black')
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet('background-color: #F8F8FF;')

        # Layout setup
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.button_new)
        vertical_layout.addWidget(self.button_refresh)
        vertical_layout.addWidget(self.table)

        self.setLayout(vertical_layout)

        self.populate_table()

    def open_department_item(self):
        form = DepartmentItem(self)
        form.exec_()

    def populate_table(self):
        departments = models.Department.get_all()
        self.table.setRowCount(len(departments))

        for linha, d in enumerate(departments):
            column_id = QTableWidgetItem()
            column_id.setText(str(d.id))
            column_id.setData(Qt.UserRole, d.name)

            column_name = QTableWidgetItem()
            column_name.setText(d.name)

            self.table.setItem(linha, 0, column_id)
            self.table.setItem(linha, 1, column_name)


class DepartmentItem(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Cadastro de Departamento')
        self.resize(300, 200)

        # Styling for label and inputs
        label_style = "font-size: 14px; color: #4682B4;"

        self.label_name = QLabel('Nome')
        self.label_name.setStyleSheet(label_style)

        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMaximumHeight(40)
        self.line_edit_name.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        # Styling for the "Save" button
        self.button_save = QPushButton('Salvar', self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setStyleSheet('''
            QPushButton {
                background-color: #87CEEB; /* Sky Blue */
                color: black;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00BFFF; /* Deep Sky Blue */
            }
        ''')
        self.button_save.setMinimumHeight(40)

        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Layout setup
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.label_name)
        vertical_layout.addWidget(self.line_edit_name)
        vertical_layout.addWidget(self.button_save)
        vertical_layout.addItem(spacer)

        self.setLayout(vertical_layout)

    def save(self):
        if self.line_edit_name.text() == '':
            QMessageBox.about(self, "Erro", "Campo de nome do departamento é obrigatório")
        else:
            department = models.Department()
            department.name = self.line_edit_name.text()
            department.save()


class EmployeeList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Listagem dos Funcionários')
        self.resize(800, 600)

        button_style = '''
            QPushButton {
                background-color: #4682B4;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A9BD4;
            }
        '''

        self.button_new = QPushButton('Novo', self)
        self.button_new.clicked.connect(self.open_employee_item)
        self.button_new.setStyleSheet(button_style)
        self.button_new.setMinimumHeight(40)

        self.button_refresh = QPushButton('Atualizar dados', self)
        self.button_refresh.clicked.connect(self.populate_table)
        self.button_refresh.setStyleSheet(button_style)
        self.button_refresh.setMinimumHeight(40)

        self.table = QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Salário', 'Data de Admissão', 'Data de Nascimento', 'Gênero', 'Departamento', 'Estado Civil', 'Distrito'])
        header = self.table.horizontalHeader()
        header.setStyleSheet('background-color: #F0F8FF; color: black')
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet('background-color: #F8F8FF;')

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.button_new)
        vertical_layout.addWidget(self.button_refresh)
        vertical_layout.addWidget(self.table)

        self.setLayout(vertical_layout)
        self.populate_table()

    def open_employee_item(self):
        form = EmployeeItem(self)
        form.exec_()

    def populate_table(self):
        employees = models.Employee.get_all()
        self.table.setRowCount(len(employees))

        for linha, e in enumerate(employees):
            self.table.setItem(linha, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(linha, 1, QTableWidgetItem(e.name))
            self.table.setItem(linha, 2, QTableWidgetItem(self.format_currency(e.salary)))
            self.table.setItem(linha, 3, QTableWidgetItem(str(e.admission_date)))
            self.table.setItem(linha, 4, QTableWidgetItem(str(e.birth_date)))
            self.table.setItem(linha, 5, QTableWidgetItem(e.gender))
            self.table.setItem(linha, 6, QTableWidgetItem(str(e.id_department)))
            self.table.setItem(linha, 7, QTableWidgetItem(str(e.id_marital_status)))
            self.table.setItem(linha, 8, QTableWidgetItem(str(e.id_district)))

    def format_currency(self, value):
        try:
            return f"R$ {float(value):,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        except ValueError:
            return "R$ 0,00"


class EmployeeItem(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Cadastro de Funcionário')
        self.resize(400, 600)

        label_style = "font-size: 14px; color: #4682B4;"

        self.label_name = QLabel('Nome')
        self.label_name.setStyleSheet(label_style)

        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMaximumHeight(40)
        self.line_edit_name.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_salary = QLabel('Salário')
        self.label_salary.setStyleSheet(label_style)

        self.line_edit_salary = QLineEdit(self)
        self.line_edit_salary.setMaximumHeight(40)
        self.line_edit_salary.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')
        self.line_edit_salary.setPlaceholderText("R$ 0,00")
        self.line_edit_salary.textChanged.connect(self.format_salary_input)

        self.label_admission_date = QLabel('Data de Admissão')
        self.label_admission_date.setStyleSheet(label_style)

        self.line_edit_admission_date = QLineEdit(self)
        self.line_edit_admission_date.setMaximumHeight(40)
        self.line_edit_admission_date.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_birth_date = QLabel('Data de Nascimento')
        self.label_birth_date.setStyleSheet(label_style)

        self.line_edit_birth_date = QLineEdit(self)
        self.line_edit_birth_date.setMaximumHeight(40)
        self.line_edit_birth_date.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_gender = QLabel('Sexo')
        self.label_gender.setStyleSheet(label_style)

        self.line_edit_gender = QLineEdit(self)
        self.line_edit_gender.setMaximumHeight(40)
        self.line_edit_gender.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_id_department = QLabel('Departamento')
        self.label_id_department.setStyleSheet(label_style)

        self.line_edit_id_department = QLineEdit(self)
        self.line_edit_id_department.setMaximumHeight(40)
        self.line_edit_id_department.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_id_marital_status = QLabel('Estado Civil')
        self.label_id_marital_status.setStyleSheet(label_style)

        self.line_edit_id_marital_status = QLineEdit(self)
        self.line_edit_id_marital_status.setMaximumHeight(40)
        self.line_edit_id_marital_status.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_id_district = QLabel('Distrito')
        self.label_id_district.setStyleSheet(label_style)

        self.line_edit_id_district = QLineEdit(self)
        self.line_edit_id_district.setMaximumHeight(40)
        self.line_edit_id_district.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.button_save = QPushButton('Salvar', self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setStyleSheet('''
                    QPushButton {
                        background-color: #87CEEB; /* Sky Blue */
                        color: black;
                        border-radius: 10px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #00BFFF; /* Deep Sky Blue */
                    }
                ''')
        self.button_save.setMinimumHeight(40)

        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(20)
        vertical_layout.addWidget(self.label_name)
        vertical_layout.addWidget(self.line_edit_name)
        vertical_layout.addWidget(self.label_salary)
        vertical_layout.addWidget(self.line_edit_salary)
        vertical_layout.addWidget(self.label_admission_date)
        vertical_layout.addWidget(self.line_edit_admission_date)
        vertical_layout.addWidget(self.label_birth_date)
        vertical_layout.addWidget(self.line_edit_birth_date)
        vertical_layout.addWidget(self.label_gender)
        vertical_layout.addWidget(self.line_edit_gender)
        vertical_layout.addWidget(self.label_id_department)
        vertical_layout.addWidget(self.line_edit_id_department)
        vertical_layout.addWidget(self.label_id_marital_status)
        vertical_layout.addWidget(self.line_edit_marital_status)
        vertical_layout.addWidget(self.label_id_district)
        vertical_layout.addWidget(self.button_save)
        vertical_layout.addItem(spacer)

        self.setLayout(vertical_layout)

    def format_salary_input(self):
        text = self.line_edit_salary.text()
        # Remover todos os caracteres que não sejam dígitos
        text = re.sub(r'[^\d]', '', text)

        if text:
            text = f"{int(text):,}".replace(",", ".")
            formatted_text = f"R$ {text}"
        else:
            formatted_text = "R$ 0,00"

        # Atualizar o campo com o valor formatado
        self.line_edit_salary.blockSignals(True)
        self.line_edit_salary.setText(formatted_text)
        self.line_edit_salary.blockSignals(False)

    def save(self):
        if self.line_edit_name.text() == '':
            QMessageBox.about(self, "Erro", "Campo de nome do funcionário é obrigatório")
        else:
            employee = models.Employee()
            employee.name = self.line_edit_name.text()
            employee.salary = float(self.line_edit_salary.text())
            employee.admission_date = self.line_edit_admission_date.text()
            employee.birth_date = self.line_edit_birth_date.text()
            employee.gender = self.label_id_department.text()
            employee.id_department = self.line_edit_id_department.text()
            employee.id_marital_status = self.label_id_marital_status.text()
            employee.id_district = self.line_edit_id_district.text()
            employee.save()

class SupplierList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Listagem dos Fornecedores')
        self.resize(600, 500)

        # Styling for the buttons
        button_style = '''
            QPushButton {
                background-color: #4682B4; /* Steel Blue */
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A9BD4; /* Lighter Steel Blue */
            }
        '''

        # Button for "New Supplier"
        self.button_new = QPushButton('Novo', self)
        self.button_new.clicked.connect(self.open_supplier_item)
        self.button_new.setStyleSheet(button_style)
        self.button_new.setMinimumHeight(40)

        # Button for "Refresh"
        self.button_refresh = QPushButton('Atualizar dados', self)
        self.button_refresh.clicked.connect(self.populate_table)
        self.button_refresh.setStyleSheet(button_style)
        self.button_refresh.setMinimumHeight(40)

        # Styling for the table
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Documento Legal'])
        header = self.table.horizontalHeader()
        header.setStyleSheet('background-color: #F0F8FF; color: black')
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet('background-color: #F8F8FF;')

        # Layout setup
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.button_new)
        vertical_layout.addWidget(self.button_refresh)
        vertical_layout.addWidget(self.table)

        self.setLayout(vertical_layout)

        self.populate_table()

    def open_supplier_item(self):
        form = SupplierItem(self)
        form.exec_()

    def populate_table(self):
        suppliers = models.Supplier.get_all()
        self.table.setRowCount(len(suppliers))

        for linha, s in enumerate(suppliers):
            column_id = QTableWidgetItem()
            column_id.setText(str(s.id))
            column_id.setData(Qt.UserRole, s.name)

            column_name = QTableWidgetItem()
            column_name.setText(s.name)

            column_legal_document = QTableWidgetItem()
            column_legal_document.setText(s.legal_document)

            self.table.setItem(linha, 0, column_id)
            self.table.setItem(linha, 1, column_name)
            self.table.setItem(linha, 2, column_legal_document)

class SupplierItem(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Cadastro de Fornecedores')
        self.resize(300, 300)

        # Styling for label and inputs
        label_style = "font-size: 14px; color: #4682B4;"

        self.label_name = QLabel('Nome')
        self.label_name.setStyleSheet(label_style)

        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMaximumHeight(40)
        self.line_edit_name.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        self.label_legal_document = QLabel('Documento Legal')
        self.label_legal_document.setStyleSheet(label_style)

        self.line_edit_legal_document = QLineEdit(self)
        self.line_edit_legal_document.setMaximumHeight(40)
        self.line_edit_legal_document.setStyleSheet('border: 1px solid #4682B4; padding: 5px;')

        # Styling for the "Save" button
        self.button_save = QPushButton('Salvar', self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setStyleSheet('''
            QPushButton {
                background-color: #87CEEB; /* Sky Blue */
                color: black;
                border-radius: 10px;d
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00BFFF; /* Deep Sky Blue */
            }
        ''')
        self.button_save.setMinimumHeight(40)

        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Layout setup
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.label_name)
        vertical_layout.addWidget(self.line_edit_name)
        vertical_layout.addWidget(self.label_legal_document)
        vertical_layout.addWidget(self.line_edit_legal_document)
        vertical_layout.addWidget(self.button_save)
        vertical_layout.addItem(spacer)

        self.setLayout(vertical_layout)

    def save(self):
        if self.line_edit_name.text() == '':
            QMessageBox.about(self, "Erro", "Campo de nome do fornecedor é obrigatório")
        else:
            supplier = models.Supplier()
            supplier.name = self.line_edit_name.text()
            supplier.legal_document = self.line_edit_legal_document.text()
            supplier.save()


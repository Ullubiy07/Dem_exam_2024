import csv
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStyleFactory, QLineEdit, QLabel, QPushButton, QCheckBox,
                             QMessageBox)


class UsersWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(145, 100, 1650, 1000)
        self.setWindowTitle('Пользователи')

        self.create_table()
        self.full_table()
        self.table_buttons()

    def checking(func):
        def inner(self, *args):
            try:
                func(self)
            except Exception as error:
                self.error_join = QMessageBox()
                self.error_join.setWindowTitle('Ошибка')
                self.error_join.setText(f'Поместите файл data.csv в папку с .exe файлом или проектом \n {error}')
                self.error_join.setIcon(QMessageBox.Information)
                self.error_join.setStandardButtons(QMessageBox.Ok)
                self.error_join.exec_()
        return inner


    def create_table(self):
        self.table = QtWidgets.QTableWidget(self)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setFont(QtGui.QFont('Arial', 12))
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 300)

        self.table.setHorizontalHeaderLabels(['Имя', 'Логин', 'Пароль'])
        self.table.horizontalHeader().setFixedHeight(60)
        self.table.setGeometry(400, 200, 920, 400)

        self.table.setStyleSheet('QScrollBar:vertical'
                                 '{'
                                 'background: rgb(200, 200, 200)'
                                 '}'
                                 'QScrollBar::handle:vertical'
                                 '{'
                                 'background-color: rgb(100, 100, 100)'
                                 '}')

        self.table.setStyleSheet("background-color: rgb(160, 160, 160);")


        massive, count = ['Имя', 'Логин', 'Пароль'], 0
        for i in massive:
            item = QtWidgets.QTableWidgetItem(i)
            item.setBackground(QtGui.QColor(200, 200, 200))
            self.table.setHorizontalHeaderItem(count, item)
            count += 1

        self.table.horizontalHeaderItem(0).setFont(QtGui.QFont('Arial', 15))
        self.table.horizontalHeaderItem(1).setFont(QtGui.QFont('Arial', 15))
        self.table.horizontalHeaderItem(2).setFont(QtGui.QFont('Arial', 15))

    @checking
    def full_table(self):
        with open('data.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)

            rows = -1
            for values in file_reader:
                values = ''.join(values).split(';')
                self.table.setRowCount(rows + 1)

                self.table.setItem(rows, 0, QtWidgets.QTableWidgetItem(values[0]))
                self.table.setItem(rows, 1, QtWidgets.QTableWidgetItem(values[1]))
                self.table.setItem(rows, 2, QtWidgets.QTableWidgetItem(values[2]))
                rows += 1

    def table_buttons(self):
        self.button_exit = QPushButton('НАЗАД', self)
        self.button_exit.setGeometry(100, 850, 100, 70)
        self.button_exit.setFont(QtGui.QFont('Arial', 12))
        self.button_exit.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.button_exit.clicked.connect(self.exit_from_Users_window)

        self.button_add = QPushButton('Добавить', self)
        self.button_add.setFont(QtGui.QFont('Arial', 12))
        self.button_add.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.button_add.setGeometry(130, 650, 260, 70)
        self.button_add.clicked.connect(self.add_user)

        self.button_change = QPushButton('Изменить', self)
        self.button_change.setFont(QtGui.QFont('Arial', 12))
        self.button_change.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.button_change.setGeometry(420, 650, 260, 70)
        self.button_change.clicked.connect(self.change_user)

        self.button_delete = QPushButton('Удалить', self)
        self.button_delete.setFont(QtGui.QFont('Arial', 12))
        self.button_delete.setStyleSheet('background-color: rgb(200, 200, 200)')
        self.button_delete.setGeometry(710, 650, 260, 70)
        self.button_delete.clicked.connect(self.delete_user)

    def delete_user(self):
        if self.table.selectedIndexes():
            self.selected_row = self.table.currentIndex().row()
            self.table.removeRow(self.selected_row)
            self.remove_from_data()

    @checking
    def remove_from_data(self):
        data_save = []
        with open('data.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)

            for i in file_reader:
                data_save.append(i)


        file = open('data.csv', 'w', encoding='utf-8')
        file.truncate()

        count = -1
        with open('data.csv', 'w', newline='', encoding='utf-8') as file:
            file = csv.writer(file)
            for i in data_save:
                if count != self.selected_row:
                    file.writerow(i)
                count += 1

    def add_user(self):
        self.func = 'Добавить'

        self.selected_name = ''
        self.selected_login = ''
        self.selected_password = ''

        self.add_user_window = AddUser(self)
        self.add_user_window.show()
        self.close()

    def change_user(self):
        if self.table.selectedIndexes():
            self.func = 'Изменить'
            self.change_row = self.table.currentIndex().row()
            self.selected_name = self.table.item(self.change_row, 0).text()
            self.selected_login = self.table.item(self.change_row, 1).text()
            self.selected_password = self.table.item(self.change_row, 2).text()

            self.change_user_window = AddUser(self)
            self.change_user_window.show()
            self.close()


    def exit_from_Users_window(self):
        from Main_window import MainWindow
        home = MainWindow()
        home.show()
        self.close()




class AddUser(QtWidgets.QDialog):
    def __init__(self, users_data=None):
        super().__init__()

        self.users_data = users_data
        self.setGeometry(145, 100, 1650, 1000)
        self.setWindowTitle('Данные пользователя')

        self.inputs()
        self.lines()
        self.buttons()

    def inputs(self):
        self.login_input = QLineEdit(self)
        self.login_input.setGeometry(750, 200, 500, 80)
        self.login_input.setFont(QtGui.QFont('Arial', 20))
        self.login_input.setText(self.users_data.selected_login)

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(750, 350, 500, 80)
        self.password_input.setFont(QtGui.QFont('Arial', 20))
        self.password_input.setText(self.users_data.selected_password)

        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(750, 500, 500, 80)
        self.name_input.setFont(QtGui.QFont('Arial', 20))
        self.name_input.setText(self.users_data.selected_name)

    def lines(self):
        self.login_line = QLabel('Логин:', self)
        self.login_line.setGeometry(500, 200, 100, 50)
        self.login_line.setFont(QtGui.QFont('Arial', 35))
        self.login_line.adjustSize()

        self.password_line = QLabel('Пароль:', self)
        self.password_line.setGeometry(455, 350, 100, 50)
        self.password_line.setFont(QtGui.QFont('Arial', 35))
        self.password_line.adjustSize()

        self.name_line = QLabel('Имя:', self)
        self.name_line.setGeometry(545, 500, 100, 50)
        self.name_line.setFont(QtGui.QFont('Arial', 35))
        self.name_line.adjustSize()

    def buttons(self):
        self.button_apply = QPushButton('ПРИНЯТЬ', self)
        self.button_apply.setFont(QtGui.QFont('Arial', 13))
        self.button_apply.setGeometry(875, 700, 250, 70)
        self.button_apply.clicked.connect(self.apply_users_data)

        self.button_back = QPushButton('НАЗАД', self)
        self.button_back.setGeometry(100, 850, 100, 70)
        self.button_back.setFont(QtGui.QFont('Arial', 12))
        self.button_back.clicked.connect(self.back_to_users_window)

    def back_to_users_window(self):
        self.back = UsersWindow()
        self.back.show()
        self.close()

    def apply_users_data(self):
        if self.login_input.text() == '' or self.password_input.text() == '' or self.name_input.text() == '':
            self.errors()
        else:
            if self.users_data.func == 'Добавить':
                with open('data.csv', 'a', encoding='utf-8', newline='') as file:
                    file_add = csv.writer(file, delimiter=';')
                    file_add.writerow([self.login_input.text(), self.password_input.text(), self.name_input.text()])
            else:
                data_save = []
                with open('data.csv', 'a+', encoding='utf-8') as file:
                    file.seek(0)
                    file_reader = csv.reader(file)

                    for i in file_reader:
                        n = ''.join(i).split(';')
                        if self.users_data.selected_name == n[0] and self.users_data.selected_login == n[1] and self.users_data.selected_password == n[2]:
                            login_change = self.login_input.text()
                            password_change = self.password_input.text()
                            name_change = self.name_input.text()
                            data_save.append([f'{name_change};{login_change};{password_change}'])
                        else:
                            data_save.append(i)
                file = open('data.csv', 'w', encoding='utf-8')
                file.truncate()

                with open('data.csv', 'w', encoding='utf-8', newline='') as file:
                    file_write = csv.writer(file)

                    for i in data_save:
                        file_write.writerow(i)
            self.back_to_users_window()



    def errors(self):
        self.empty = QMessageBox()
        self.empty.setIcon(QMessageBox.Information)
        self.empty.setWindowTitle('Ошибка')
        self.empty.setStandardButtons(QMessageBox.Ok)
        if self.login_input.text() == '':
            self.empty.setText('Введите логин')
        elif self.password_input.text() == '':
            self.empty.setText('Введите пароль')
        elif self.name_input.text() == '':
            self.empty.setText('Введите имя')
        self.empty.exec_()


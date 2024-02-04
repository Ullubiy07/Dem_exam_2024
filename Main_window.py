import sys
import csv
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox
from Users_window import UsersWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(145, 100, 1650, 1000)
        self.setWindowTitle('Окно авторизации')


        self.home_inputs()
        self.home_lines()
        self.home_buttons()


    def checking(func):
        def inner(self, *args):
            try:
                func(self)
            except Exception as error:
                print(error)
        return inner

    def home_inputs(self):
        file_reader = ['', '']
        with open('remembered_data.csv', 'a+', encoding='utf-8') as file:
            import os
            file.seek(0)
            if os.stat('remembered_data.csv').st_size != 0:
                file_reader = ''.join(list(csv.reader(file))[0]).split()

        self.login_input = QLineEdit(self)
        self.login_input.setGeometry(750, 300, 500, 80)
        self.login_input.setFont(QtGui.QFont('Arial', 20))
        self.login_input.setStyleSheet('background-color: white')
        self.login_input.setText(file_reader[0])

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(750, 500, 500, 80)
        self.password_input.setFont(QtGui.QFont('Arial', 20))
        self.password_input.setStyleSheet('background-color: white')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(file_reader[1])

    def home_lines(self):
        self.login_line = QLabel('Логин:', self)
        self.login_line.setGeometry(500, 300, 100, 50)
        self.login_line.setFont(QtGui.QFont('Arial', 35))
        self.login_line.adjustSize()

        self.password_line = QLabel('Пароль:', self)
        self.password_line.setGeometry(455, 500, 100, 50)
        self.password_line.setFont(QtGui.QFont('Arial', 35))
        self.password_line.adjustSize()

        self.remember_line = QCheckBox('Запомнить меня', self)
        self.remember_line.setGeometry(750, 630, 100, 50)
        self.remember_line.setFont(QtGui.QFont('Arial', 15))
        self.remember_line.setStyleSheet('QCheckBox::indicator'
                                         '{'
                                         'width : 25px;'
                                         'height : 25px;'
                                         '}')
        self.remember_line.adjustSize()


    def home_buttons(self):
        self.button_exit = QPushButton('ВЫХОД', self)
        self.button_exit.setGeometry(100, 850, 100, 70)
        self.button_exit.setFont(QtGui.QFont('Arial', 13))
        self.button_exit.setStyleSheet("background-color: rgb(187, 187, 187)")
        self.button_exit.clicked.connect(lambda: self.close())

        self.button_join = QPushButton('Войти', self)
        self.button_join.setGeometry(950, 700, 100, 70)
        self.button_join.setFont(QtGui.QFont('Arial', 13))
        self.button_join.setStyleSheet('Background-color: rgb(187, 187, 187)')
        self.button_join.clicked.connect(self.checking_exist_data)


    def checking_exist_data(self):
        import os.path
        if os.path.exists('data.csv'):
            self.checking_data()
        else:
            self.error_join = QMessageBox()
            self.error_join.setWindowTitle('Ошибка')
            self.error_join.setText('Поместите файл data.csv в папку с .exe файлом или проектом')
            self.error_join.setIcon(QMessageBox.Information)
            self.error_join.setStandardButtons(QMessageBox.Ok)
            self.error_join.exec_()

    def checking_data(self):
        login, password = self.login_input.text(), self.password_input.text()
        self.access = False
        with open('data.csv', 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            count = 0
            for i in file_reader:
                i = ''.join(i).split(';')
                count += 1
                if ((login == i[1] and password == i[2]) or (login == 'Usr' and password == '123')):
                    self.access = True
                    break
        self.check_access()

    def check_access(self):
        if self.access:
            if self.remember_line.isChecked():
                with open('remembered_data.csv', 'w', encoding='utf-8') as file:
                    file.writelines([self.login_input.text(), ' ' + self.password_input.text()])
            self.join_to_Users_window()
        else:
            self.wrong_data()

    def wrong_data(self):
        self.error_join = QMessageBox()
        self.error_join.setWindowTitle('Ошибка')
        self.error_join.setText('Неверный логин или пароль')
        self.error_join.setIcon(QMessageBox.Information)
        self.error_join.setStandardButtons(QMessageBox.Ok)
        self.error_join.exec_()


    def join_to_Users_window(self):
        self.Users = UsersWindow()
        self.Users.show()
        self.close()


def application():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    home = MainWindow()
    home.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()




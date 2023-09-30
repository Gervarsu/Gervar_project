import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QGroupBox, QHBoxLayout, QStackedWidget, QTabWidget, QMessageBox

# Создание базы данных SQLite
conn = sqlite3.connect('tk1/users.sql')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        histori TEXT
    )
''')
conn.commit()

class RegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Вход/Регистрация :3')
        self.username_label = QLabel('Имя пользователя:')
        self.username_entry = QLineEdit()
        self.password_label = QLabel('Пароль:')
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_repeat_label = QLabel('Повторите пароль:')
        self.password_repeat_entry = QLineEdit()
        self.password_repeat_entry.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Зарегистрироваться')
        self.register_button.clicked.connect(self.register_user)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.password_repeat_label)
        layout.addWidget(self.password_repeat_entry)
        layout.addWidget(self.register_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        password_repeat = self.password_repeat_entry.text()

        # Проверка, что поля не пусты
        if not username or not password or not password_repeat:
            self.result_label.setText("Заполните все поля")
            return

        # Проверка совпадения паролей
        if password != password_repeat:
            self.result_label.setText("Пароли не совпадают")
            return

        # Проверка на уникальность имени пользователя
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            self.result_label.setText("Пользователь уже существует")
            return

        # Вставка нового пользователя в базу данных
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        self.result_label.setText("Регистрация успешна")

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.username_label = QLabel('Имя пользователя:')
        self.username_entry = QLineEdit()
        self.password_label = QLabel('Пароль:')
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.login_user)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        # Проверка, что поля не пусты
        if not username or not password:
            self.result_label.setText("Заполните все поля")
            return

        # Поиск пользователя в базе данных
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self.result_label.setText("Вход успешен")
            self.open_another_file()
        else:
            self.result_label.setText("Неправильное имя пользователя или пароль")

    def open_another_file(self):
        # Откройте другой Python-файл здесь, например:
        import os
        os.system("python tk1/weather_app.py")
        pass

class MainWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        registration_tab = RegistrationWidget()
        login_tab = LoginWidget()

        self.addTab(registration_tab, "Регистрация")
        self.addTab(login_tab, "Вход")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('tk1/logo.ico'))
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())

# Закрытие базы данных SQLite
conn.close()
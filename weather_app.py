import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser, QStackedWidget, QFrame, QButtonGroup, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = 'af2c77fe5a5fae309afdcc4a63a56bd8'
        self.background_color = '#444'  # Задний фон по умолчанию - темно-серый
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Погода :3')
        self.setGeometry(100, 100, 800, 600)  # Уменьшаем размер окна

        layout = QVBoxLayout()  # Изменяем главный макет на вертикальный
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы по краям

        # Перемещаем панель навигации наверх
        self.create_navigation_panel()
        layout.addWidget(self.navigation_panel)

        self.central_layout = QVBoxLayout()
        layout.addLayout(self.central_layout)

        # Создаем виджет для отображения разных разделов (Погода, История, Новости)
        self.stacked_widget = QStackedWidget()
        self.central_layout.addWidget(self.stacked_widget)

        # Погода
        self.weather_widget = QWidget()
        self.create_weather_ui()
        self.stacked_widget.addWidget(self.weather_widget)

        # История (здесь можно добавить функциональность для отображения истории)
        self.history_widget = QWidget()
        self.create_history_ui()
        self.stacked_widget.addWidget(self.history_widget)

        # Новости (здесь можно добавить функциональность для отображения новостей)
        self.news_widget = QWidget()
        self.create_news_ui()
        self.stacked_widget.addWidget(self.news_widget)

        self.setLayout(layout)

        # Сделаем погоду активной по умолчанию
        self.show_weather()

    def create_navigation_panel(self):
        self.navigation_panel = QFrame()
        self.navigation_panel.setFrameShape(QFrame.Panel)
        self.navigation_panel.setFrameShadow(QFrame.Sunken)

        # Кнопки для переключения между разделами с символьными иконками
        layout = QHBoxLayout()

        self.weather_button = QPushButton(QIcon('tk1/weather.png'), 'Погода')
        layout.addWidget(self.weather_button)
        self.weather_button.clicked.connect(self.show_weather)  # Связываем сигнал нажатия кнопки с методом

        self.history_button = QPushButton(QIcon('tk1/history.png'), 'История')
        layout.addWidget(self.history_button)
        self.history_button.clicked.connect(self.show_history)  # Связываем сигнал нажатия кнопки с методом

        self.news_button = QPushButton(QIcon('tk1/news.png'), 'Новости')
        layout.addWidget(self.news_button)
        self.news_button.clicked.connect(self.show_news)  # Связываем сигнал нажатия кнопки с методом

        self.navigation_panel.setLayout(layout)

    def create_weather_ui(self):
        layout = QVBoxLayout()

        self.city_label = QLabel('Введите название города:')
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        layout.addWidget(self.city_input)

        self.weather_label = QLabel('Погода сегодня:')
        layout.addWidget(self.weather_label)

        self.weather_text = QTextBrowser()
        layout.addWidget(self.weather_text)

        self.get_weather_button = QPushButton('Получить погоду')
        layout.addWidget(self.get_weather_button)
        self.get_weather_button.clicked.connect(self.get_weather)

        self.weather_widget.setLayout(layout)

    def create_history_ui(self):
        # Здесь можно добавить интерфейс для отображения истории
        layout = QVBoxLayout()
        label = QLabel("История")
        layout.addWidget(label)
        self.history_widget.setLayout(layout)

    def create_news_ui(self):
        # Здесь можно добавить интерфейс для отображения новостей
        layout = QVBoxLayout()
        label = QLabel("Новости")
        layout.addWidget(label)
        self.news_widget.setLayout(layout)

    def show_weather(self):
        self.stacked_widget.setCurrentWidget(self.weather_widget)

    def show_history(self):
        self.stacked_widget.setCurrentWidget(self.history_widget)

    def show_news(self):
        self.stacked_widget.setCurrentWidget(self.news_widget)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            self.weather_text.setPlainText('Введите название города!')
            return

        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&lang=ru'

        try:
            response = requests.get(url)
            data = response.json()
            if data['cod'] == 200:
                temperature_kelvin = data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15
                weather_description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                wind_speed = data['wind']['speed']

                weather_info = f'Температура: {temperature_celsius:.2f}°C\n' \
                               f'Состояние: {weather_description.capitalize()}\n' \
                               f'Влажность: {humidity}%\n' \
                               f'Давление: {pressure} hPa\n' \
                               f'Скорость ветра: {wind_speed} м/с'
                self.weather_text.setPlainText(weather_info)
            else:
                self.weather_text.setPlainText('Город не найден!')
        except Exception as e:
            self.weather_text.setPlainText(f'Ошибка при запросе к API: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('tk1/logo.ico'))
    window = WeatherApp()
    
    # Устанавливаем стиль для полностью темной темы
    app.setStyleSheet(f"""
        QPushButton {{
            background-color: {window.background_color};
            color: #FFF;
            border-radius: 2px;
        }}
        
        QLabel, QLineEdit, QTextBrowser {{
            background-color: {window.background_color};
            color: #FFF;
            border-radius: 2px;
        }}
        
        QTextBrowser {{
            border: 1px solid #444;
        }}
    """)
    
    window.show()
    sys.exit(app.exec_())

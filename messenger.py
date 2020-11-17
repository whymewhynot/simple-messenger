from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import messenger_ui

class MessengerWindow(QtWidgets.QMainWindow, messenger_ui.Ui_MainWindow):

    def __init__(self, server):
        super().__init__()
        self.setupUi(self)

        self.server = server

        self.send.pressed.connect(self.send_message)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display_messages)
        self.timer.start(1000)

        self.after = 0

    def send_message(self):
        name = self.name.text()
        text = self.text.toPlainText()
        data = {"name": name, "text": text}
        try:
            response = requests.post(f"{self.server}/send", json=data)
        except:
            self.messages.append("Ошибка: сервер недоступен... Попробуйте позже\n")
            self.messages.repaint()
            return

        if response.status_code != 200:
            self.messages.append("Ошибка: пустое сообщение или имя пользователя\n")
            self.messages.repaint()
            return

        self.text.setText("")
        self.text.repaint()

    def format_message(self, message):
        message_time = datetime.fromtimestamp(message["time"]).strftime("%H:%M %d.%m.%Y")
        self.messages.append(f"{message_time}\n{message['name']}: {message['text']}\n")
        self.messages.repaint()

    def display_messages(self):
        try:
            data = requests.get(f"{self.server}/messages",
                                params={"after": self.after}).json()
        except:
            return
        for message in data["messages"]:
            self.format_message(message)
            self.after = message["time"]

app = QtWidgets.QApplication([])
window = MessengerWindow(server = "http://127.0.0.1:5000/")
window.show()
app.exec_()
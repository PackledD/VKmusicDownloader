from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from urllib.request import urlopen
import sys


class Captcha(QMainWindow):

    def __init__(self, captcha, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Captcha")
        self.resize(333, 207)

        self.captcha = QLabel()
        url = captcha.get_url()
        data = urlopen(url).read()
        img = QPixmap()
        img.loadFromData(data)
        self.captcha.setPixmap(img)

        self.input = QLineEdit()
        self.input.setMinimumSize(QSize(150, 20))
        self.input.setMaximumSize(QSize(150, 20))

        self.button = QPushButton("Log in")
        self.button.setFont(QFont("Arial", 13))
        self.button.setMinimumSize(QSize(75, 25))
        self.button.setMaximumSize(QSize(125, 25))
        self.button.clicked.connect(self.send)

        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(self.captcha)

        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.input)

        layoutH3 = QHBoxLayout()
        layoutH3.addWidget(self.button)

        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH1)
        layoutV.addLayout(layoutH2)
        layoutV.addLayout(layoutH3)

        centerWidget = QWidget()
        centerWidget.setLayout(layoutV)
        self.setCentralWidget(centerWidget)

    def send(self):
        with open('temp.txt', 'w') as f:
            f.write(self.input.text())
        self.close()

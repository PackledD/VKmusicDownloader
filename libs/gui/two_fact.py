from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class Two_fact(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Captcha")
        self.resize(333, 150)

        label = QLabel("Enter two-factor code: ")
        label.setFont(QFont("Arial", 15))
        label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

        self.remember = QCheckBox('Remember this device?', self)
        self.remember.stateChanged.connect(lambda state: self.change_state(state))
        self.memory = False

        self.input = QLineEdit()
        self.input.setMinimumSize(QSize(150, 20))
        self.input.setMaximumSize(QSize(150, 20))

        self.button = QPushButton("Log in")
        self.button.setFont(QFont("Arial", 13))
        self.button.setMinimumSize(QSize(75, 25))
        self.button.setMaximumSize(QSize(125, 25))
        self.button.clicked.connect(self.send)

        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(label)

        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.input)

        layoutH3 = QHBoxLayout()
        layoutH3.addWidget(self.button)

        layoutH4 = QHBoxLayout()
        layoutH4.addWidget(self.remember)

        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH1)
        layoutV.addLayout(layoutH2)
        layoutV.addLayout(layoutH3)
        layoutV.addLayout(layoutH4)

        centerWidget = QWidget()
        centerWidget.setLayout(layoutV)
        self.setCentralWidget(centerWidget)

    def change_state(self, state):
        if state == Qt.Checked:
            self.memory = True
        else:
            self.memory = False

    def send(self):
        with open('temp.tmp', 'w') as f:
            f.write(self.input.text() + '\n')
            f.write(str(self.memory))
        self.close()

import sys
sys.path.insert(0, "..")
import auth
import music
import mainroot
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Log_root(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Login")
        self.resize(333, 207)

        # self.console = None

        label_log = QLabel("Login: ")
        label_log.setAlignment(Qt.AlignRight)

        label_pas = QLabel("Password: ")
        label_pas.setAlignment(Qt.AlignRight)

        self.errors = QLabel("")
        self.errors.setAlignment(Qt.AlignRight)

        label_log.setFont(QFont('Arial', 15))
        label_pas.setFont(QFont('Arial', 15))
        self.errors.setFont(QFont('Arial', 15))

        loginButton = QPushButton("Log in")
        loginButton.setFont(QFont("Arial", 13))
        loginButton.setMinimumSize(QSize(75, 25))
        loginButton.setMaximumSize(QSize(125, 25))
        loginButton.clicked.connect(self.authorization)

        self.inputLogin = QLineEdit()
        self.inputLogin.setMinimumSize(QSize(150, 20))
        self.inputLogin.setMaximumSize(QSize(150, 20))

        self.inputPassword = QLineEdit()
        self.inputPassword.setMinimumSize(QSize(150, 20))
        self.inputPassword.setMaximumSize(QSize(150, 20))

        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(label_log)
        layoutH1.addWidget(self.inputLogin)

        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(label_pas)
        layoutH2.addWidget(self.inputPassword)

        layoutH3 = QHBoxLayout()
        layoutH3.addWidget(self.errors)
        layoutH3.addWidget(loginButton)

        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH1)
        layoutV.addLayout(layoutH2)
        layoutV.addLayout(layoutH3)

        centerWidget = QWidget()
        centerWidget.setLayout(layoutV)
        self.setCentralWidget(centerWidget)

    def authorization(self):
        login = self.inputLogin.text()
        password = self.inputPassword.text()
        try:
            self.user = auth.auth(login, password)
            self.user.session_start()
            self.mainroot = mainroot.Root(self.user)
            music.get_songs_info(self.user)
            self.mainroot.show()
            self.mainroot.get_all_songs()
            self.close()
        except Exception as err:
            self.errors.setText(str(err))
            self.errors.setFont(QFont('Arial', 12))
            self.errors.setStyleSheet("color: rgb(255, 0, 0)")

import sys
sys.path.insert(0, "..")
import music
import auth
import os
import json
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Root(QMainWindow):

    def __init__(self, user, parent=None):
        super().__init__(parent)

        self.path = '.'
        self.user = user

        # self.console = QPlainTextEdit()
        # self.console.setReadOnly(True)
        # self.console.setFont(QFont('Arial', 11))

        self.to_download = []
        self.music = QListWidget(self)
        self.music.itemActivated.connect(self.change)

        self.progress = QProgressBar()

        openDirButton = QPushButton("Open")
        openDirButton.clicked.connect(self.getDirectory)

        saveOneButton = QPushButton("Save")
        saveOneButton.clicked.connect(self.download)

        saveAllButton = QPushButton("Save all")
        saveAllButton.clicked.connect(self.download_all)

        removeSelButton = QPushButton("Remove selection")
        removeSelButton.clicked.connect(self.deselect)

        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(openDirButton)
        layoutV1.addWidget(saveOneButton)
        layoutV1.addWidget(saveAllButton)
        layoutV1.addWidget(removeSelButton)

        layoutV2 = QVBoxLayout()
        layoutV2.addWidget(self.music)
        layoutV2.addWidget(self.progress)
        # layoutV2.addWidget(self.console)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV1)
        layoutH.addLayout(layoutV2)

        centerWidget = QWidget()

        centerWidget.setLayout(layoutH)
        self.setCentralWidget(centerWidget)

        self.resize(900, 640)
        self.setWindowTitle("VK music downloader")

    def getDirectory(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.path = dirlist

    def download(self):
        counter = 0
        max_counter = len(self.to_download)
        self.progress.setMaximum(max_counter)
        for i in self.to_download:
            music.download_song(i, self.user, self.path)
            counter += 1
            self.progress.setValue(counter)
        self.progress.reset()

    def download_all(self):
        dirr = './data/{0}/Normal_Songs'.format(self.user.user_id)
        files = os.listdir(dirr)
        counter = 0
        max_counter = len(files)
        self.progress.setMaximum(max_counter)
        for i in files:
            music.download_song(i[:-5], self.user, self.path)
            counter += 1
            self.progress.setValue(counter)
        self.progress.reset()

    def deselect(self):
        for i in range(self.music.count()):
            item = self.music.item(i)
            self.music.itemWidget(item).setCheckState(0)

    # def write_to_console(self):
    #     with open('./log/last_log.txt', 'r') as log:
    #         cur = log.read()
    #         self.console.setPlainText(cur)

    def get_all_songs(self):
        dirr = './data/{0}/Normal_Songs'.format(self.user.user_id)
        files = os.listdir(dirr)
        for i in files:
            with open(dirr + '/' + i, 'r') as f:
                cur_song = json.load(f)
                # загрузка песни и помещение ее в чекбокс
                new_song = QCheckBox(f'{cur_song["artist"]} - {cur_song["title"]}', self)
                new_song.stateChanged.connect(
                    lambda state=new_song.isChecked(), song=i[:-5]: self.change(state, song)
                )
                new_song.setFont(QFont('Arial', 13))
                item = QListWidgetItem(self.music)  # ???
                self.music.addItem(item)
                self.music.setItemWidget(item, new_song)

    def change(self, state, song):
        if (state == Qt.Checked) and (song not in self.to_download):
            self.to_download.append(song)
        elif song in self.to_download:
            self.to_download.remove(song)

# user = auth.auth('qw', 'qw')
# app = QApplication(sys.argv)
# ex = Root(user)
# ex.get_all_songs()
# ex.show()
# sys.exit(app.exec_())

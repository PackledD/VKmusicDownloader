import sys
sys.path.insert(0, "..")
import music
import auth
import os
import json
from log import Logging
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import threading


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
        saveOneButton.clicked.connect(lambda: threading.Thread(target=self.download).start())

        selectAllButton = QPushButton("Select all")
        selectAllButton.clicked.connect(lambda: threading.Thread(target=self.select_all).start())

        removeSelButton = QPushButton("Remove selection")
        removeSelButton.clicked.connect(self.deselect)

        reloadMusic = QPushButton("Reload music")
        reloadMusic.clicked.connect(self.reload_music)

        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(openDirButton)
        layoutV1.addWidget(saveOneButton)
        layoutV1.addWidget(selectAllButton)
        layoutV1.addWidget(removeSelButton)
        layoutV1.addWidget(reloadMusic)

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

    def reload_music(self):
        self.to_download = []
        self.music = QListWidget(self)
        self.music.itemActivated.connect(self.change)
        music.get_songs_info(self.user)
        self.get_all_songs()

    def getDirectory(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.path = dirlist

    def download(self):
        counter = 0
        counter_broak = 0
        max_counter = len(self.to_download)
        self.progress.setMinimum(counter)
        self.progress.setMaximum(max_counter)
        for i in self.to_download:
            try:
                music.download_song(i, self.user, self.path)
                counter += 1
            except OSError:
                Logging("Can't download song: {0}".format(i[:-5:]), self.user.logfile)
                counter_broak += 1
            self.progress.setValue(counter)
        self.progress.reset()
        text_info = '''Complete downloading. Total: {0}. Successful: {1}. Broak: {2}'''.format(
            max_counter, counter, counter_broak)
        Logging(text_info, self.user.logfile)
        # qw = QMessageBox(self)
        # qw.setWindowTitle('Info')
        # qw.setText(text_info)
        # qw.setIcon(QMessageBox.Information)
        # qw.setStandardButtons(QMessageBox.Ok)
        # qw.show()
        self.deselect()

    def select_all(self):
        for i in range(self.music.count()):
            item = self.music.item(i)
            self.music.itemWidget(item).setCheckState(2)

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

# user = auth.auth('qw', 'qw', False)
# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(True)
# ex = Root(user)
# ex.get_all_songs()
# ex.show()
# sys.exit(app.exec_())

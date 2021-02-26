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
from tools import resource_path


class Root(QMainWindow):

    def __init__(self, user, parent=None):
        super().__init__(parent)

        self.resize(900, 640)
        self.setWindowTitle("VK music downloader")
        self.setWindowIcon(QIcon(resource_path('logo.png')))

        self.path = '.'
        self.user = user

        self.to_download = []
        self.music = QListWidget(self)
        self.music.itemActivated.connect(self.change)

        self.progress = QProgressBar()

        self.info = QLabel("{0} find. {1} select".format(0, 0))
        self.info.setFont(QFont('Arial', 13))

        openDirButton = QPushButton("Open")
        openDirButton.clicked.connect(self.getDirectory)

        saveOneButton = QPushButton("Save")
        saveOneButton.clicked.connect(lambda: threading.Thread(target=self.download).start())

        selectAllButton = QPushButton("Select all")
        selectAllButton.clicked.connect(self.select_all)

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
        layoutV2.addWidget(self.info)
        layoutV2.addWidget(self.music)
        layoutV2.addWidget(self.progress)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV1)
        layoutH.addLayout(layoutV2)

        centerWidget = QWidget()

        centerWidget.setLayout(layoutH)
        self.setCentralWidget(centerWidget)

    def reload_music(self):
        self.to_download.clear()
        self.music.clear()
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
        # self.deselect()  # crash!!!

    def select_all(self):
        for i in range(self.music.count()):
            item = self.music.item(i)
            self.music.itemWidget(item).setCheckState(2)

    def deselect(self):
        for i in range(self.music.count()):
            item = self.music.item(i)
            self.music.itemWidget(item).setCheckState(0)

    def get_all_songs(self):
        try:
            dirr = './data/{0}/Normal_Songs'.format(self.user.user_id)
            files = os.listdir(dirr)
        except OSError:
            files = []
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
        self.info.setText("{0} find. {1} select".format(len(files), 0))

    def change(self, state, song):
        if (state == Qt.Checked) and (song not in self.to_download):
            self.to_download.append(song)
        elif song in self.to_download:
            self.to_download.remove(song)
        cur = str(self.info.text())
        ind0 = cur.index('.') + 1
        ind1 = cur.index(' select')
        self.info.setText(cur[:ind0:] + str(len(self.to_download)) + cur[ind1::])

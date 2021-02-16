import sys
import os
import vk_api
from vk_api import audio
from log import Logging, clear_last_log
import tools
import json
# from time import sleep
sys.path.insert(0, "./gui")
# import captcha
# import two_fact
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    # app = QApplication(sys.argv)
    # ui = captcha.Captcha(captcha)
    # ui.show()
    # ui.send()
    # sys.exit(app.exec_())
    # # if not os.path.exists('temp.txt'):
    # #     sleep(1)
    # with open('temp.txt', 'r') as f:
    #     key = f.read().strip()
    return(captcha.try_again(key))


def two_factor_auth_handler():
    key = input("Enter authentication code: ")
    # app = QApplication(sys.argv)
    # ui = two_fact.Two_fact()
    # ui.show()
    # while not os.path.exists('temp.txt'):
    #     sleep(1)
    # with open('temp.txt', 'r') as f:
    #     key = f.read().strip()
    remember_device = True
    return(key, remember_device)


class auth():
    """This class make VK authorization"""
    session = None
    music = None
    api = None
    logfile = 'last_log.txt'
    user_id = 0

    def __init__(self, login, password, relog):
        if os.path.exists('user.json') and relog is True:
            with open('user.json', 'r') as f:
                user_data = json.load(f)
                self.login = user_data['login']
                self.password = tools.decode(user_data['password'])
        else:
            self.login = str(login)
            self.password = str(password)

    def set_logfile_name(self):
        self.logfile = 'log-{0}--{1}.txt'.format(
            tools.get_formated_date(),
            tools.get_formated_time().replace(':', '-')
        )
        return(self)

    def get_id(self):
        with open('vk_config.json') as f_id:
            cur = json.load(f_id)
            for i in range(3):
                key = str(list(cur.keys())[0])
                if i == 0:
                    cur = cur[key]['token']
                else:
                    cur = cur[key]
            self.user_id = int(cur['user_id'])
        return(self)

    def session_start(self):
        self.session = vk_api.VkApi(
            login=self.login,
            password=self.password,
            auth_handler=two_factor_auth_handler,
            captcha_handler=captcha_handler,
            config_filename='vk_config.json'
        )
        clear_last_log()
        self.set_logfile_name()
        Logging("Trying to start session", self.logfile)
        self.session.auth()
        Logging("Session started", self.logfile)
        Logging("Getting music api", self.logfile)
        self.api = self.session.get_api()
        self.music = audio.VkAudio(self.session)
        Logging("Complete successfully", self.logfile)
        self.get_id()
        with open('user.json', 'w') as f:
            user_data = {'login': self.login, 'password': tools.encode(self.password)}
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        return(self)

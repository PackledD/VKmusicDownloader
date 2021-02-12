import time
import os


def get_formated_date():  # Get date for logging
    cur_date = time.strftime('%Y-%b-%d', time.localtime())
    return cur_date


def get_formated_time():  # Get time for logging
    cur_time = time.strftime('%X', time.localtime())
    return cur_time


def clear_last_log():  # Clear content of file "last_log.txt"
    if os.path.exists("./log"):
        with open("log/" + "last_log.txt", 'w'):
            pass


def Logging(text, file):
    try:
        '''
        This function make logging something
        It take two arguments: text which woill place in logfile and logfile name
        Also it dupplicate new log inta "last_log.txt"
        '''
        if not os.path.exists("./log"):
            os.mkdir("log")
        with open("log/" + file, 'a') as f:
            f.write('[{0}][{1}]'.format(get_formated_date(),
                                        get_formated_time()) + text + '\n')
        if file != 'last_log.txt':
            Logging_last_log(text)
    except Exception:
        pass


def Logging_last_log(text):
    Logging(text, "last_log.txt")

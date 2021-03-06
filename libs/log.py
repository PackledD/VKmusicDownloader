import os
import tools


def clear_last_log():  # Clear content of file "last_log.txt"
    if os.path.exists("./log"):
        with open("log/last_log.txt", 'w'):
            pass


def Logging(text, file):
    try:
        '''
        This function make logging something
        It take two arguments: text which woill place in logfile and logfile name
        Also it dupplicate new log into "last_log.txt"
        '''
        if not os.path.exists("./log"):
            os.mkdir("log")
        p = "./log/" + file
        if not os.path.exists(p):
            with open(p, 'w'):
                pass
        with open("log/" + file, 'a') as f:
            f.write('[{0}][{1}]'.format(tools.get_formated_date(),
                                        tools.get_formated_time()) + text + '\n')
        if file != 'last_log.txt':
            Logging_last_log(text)
    except Exception:
        pass


def Logging_last_log(text):
    Logging(text, "last_log.txt")

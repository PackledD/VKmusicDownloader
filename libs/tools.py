import time
import random


def get_formated_date():  # Get date for logging
    cur_date = time.strftime('%Y-%b-%d', time.localtime())
    return cur_date


def get_formated_time():  # Get time for logging
    cur_time = time.strftime('%X', time.localtime())
    return cur_time


def make_name_normal(a):
    # Cuts illegal chars from name
    bad_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    a = ''.join(i for i in a if not i in bad_chars)
    return a


def encode(a):
    length = len(a)
    temp = list(a)
    temp_info = []
    err = False
    for i in range(length):
        cur = str(hex(ord(a[i])))  # every char to hex digit
        try:
            new_cur = cur[:2:] + cur[-1:1:-1]  # try to reverse char code (be like "\x64" -> "\x46")
            rand = random.randint(24, 62) * 2 + 1  # random digit which % 2 == 1
            temp_info.append(chr(rand))  # saving info about it
        except UnicodeEncodeError:
            err = True
            new_cur = cur
            rand = random.randint(24, 62) * 2  # random digit which % 2 == 0
            temp_info.append(chr(rand))
        temp[i] = chr(int(new_cur, 16))
    obfl = random.randint(1, 5)  # length of obfuscating chars
    if err:
        result = f'1{length}/'  # if consist errors. Decoder will check obfuscated chars (more time)
    else:
        result = f'0{length}/'  # no errors, can delete obfuscate
    for i in range(length):
        result = result + temp[i] + temp_info[i]
        for j in range(obfl):
            rand = random.randint(32, 126)
            result = result + chr(rand)
    return result


def decode(a):
    err = a[0]
    a = a[1::]
    # obfl = a[0]  # length of obfuscating chars
    # a = a[1::]
    ind = a.find('/')  # search first index of '/'
    length = int(a[:ind:])  # get length of normal string
    a = a[ind + 1::]  # cut encoded string
    if err == '1':
        pass
    else:
        obfl = len(a) // length
        result = list(a[::obfl])
        for i in range(length):
            cur = str(hex(ord(result[i])))
            cur = cur[:2:] + cur[-1:1:-1]
            result[i] = chr(int(cur, 16))  # turn it back to normal
        result = ''.join(result)
        return result

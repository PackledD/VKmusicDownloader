import time
import random
import os


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
        with open('temp.tmp', 'w') as f:
            try:
                new_cur = cur[:2:] + cur[-1:1:-1]  # try to reverse char code (be like "\x64" -> "\x46")
                f.write(chr(int(new_cur, 16)))
                rand = random.randint(24, 62) * 2 + 1  # random digit which % 2 == 1
                temp_info.append(chr(rand))  # saving info about it
            except UnicodeEncodeError:
                err = True
                new_cur = cur
                rand = random.randint(24, 62) * 2  # random digit which % 2 == 0
                temp_info.append(chr(rand))
        if os.path.isfile('./temp.tmp'):
            os.remove('temp.tmp')
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
    obfl = len(a) // length
    if err == '1':
        obfl -= 2
        count = 0
        data = []
        result = ''
        while count < len(a):
            data.append(a[count])
            data.append(a[count + 1])
            count += obfl + 2
        for i in range(len(data) // 2):
            # print(hex(ord(data[2 * i])))
            # print(ord(data[2 * i + 1]))
            cur = data[2 * i]
            info = data[2 * i + 1]
            if ord(info) % 2 == 0:
                result = result + cur
            else:
                cur = str(hex(ord(cur)))
                cur = cur[:2:] + cur[-1:1:-1]
                cur = chr(int(cur, 16))
                # print(cur)
                result = result + cur
    else:
        result = list(a[::obfl])
        for i in range(length):
            cur = str(hex(ord(result[i])))
            cur = cur[:2:] + cur[-1:1:-1]
            result[i] = chr(int(cur, 16))  # turn it back to normal
        result = ''.join(result)
    return result

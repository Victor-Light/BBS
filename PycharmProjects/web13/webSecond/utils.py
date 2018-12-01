import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('gua.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

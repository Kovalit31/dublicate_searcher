import os, sys
import time

DEBUG = True
ERROR = True
INFO = True

def debugger(message: str, objects=[], thread=None):
    global DEBUG
    start = "[DEBUG]"
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    if DEBUG:
        e_time = time.ctime()
        msg = f"\n{start}[{e_time}] " + message
        for x in range(len(objects)):
            _temp_type = type(objects[x])
            _temp_len = None
            if not _temp_type == int and not _temp_type == bool:
                _temp_len = len(objects[x])
            else:
                _temp_len = "<cannot calculate on unusual type>"
            _temp_content = objects[x]
            msg += f"\n{start}[{e_time}] Object {x} type: {_temp_type}, len: {_temp_len}, contents: {_temp_content}"
        print(msg) 

def exceptor(message: str, type="Exception", thread=None):
    global ERROR
    start = "[ERROR]"
    e_time = time.ctime()
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    if ERROR:
        print(f"{start}[{e_time}][{type.upper()}] {message}")
        sys.exit()
    else:
        sys.exit()

def info(message: str, thread=None):
    global INFO
    start = "[INFO]"
    e_time = time.ctime()
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    print(f"{start}[{e_time}] {message}")
import os, sys
import time

DEBUG = True

def debugger(message: str, objects=[], thread=None, use_time=True):
    global DEBUG
    start = "[DEBUG]"
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    if DEBUG:
        if use_time:
            e_time = "[" + str(time.ctime()) + "]"
        else:
            e_time = ""
        msg = f"\n{start}{e_time}: " + message
        for x in range(len(objects)):
            _temp_type = type(objects[x])
            _temp_len = None
            try:
                _temp_len = len(objects[x])
            except:
                _temp_len = "<cannot calculate on unusual type>"
            _temp_content = objects[x]
            msg += f"\n{start}{e_time}: Object {x} type: {_temp_type}, len: {_temp_len}, contents: {_temp_content}"
        print(msg) 

def exceptor(message: str, type=Exception, thread=None, short=False, use_time=False, exception_do=0):
    if short:
        start = "[@]"
    else:
        start = "[ERROR]"
    if use_time:
        e_time = "[" + str(time.ctime()) + "]"
    else:
        e_time = ""
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    print(f"{start}{e_time}[{str(type).upper()}]: {message}")
    if exception_do == 0:
        sys.exit()
    if exception_do == 1:
        pass
    if exception_do == 2:
        raise type(message)
   

def info(message: str, thread=None, short=False, use_time=False):
    if short:
        start = "[*]"
    else:
        start = "[INFO]"
    if use_time:
        e_time = "[" + str(time.ctime()) + "]"
    else:
        e_time = ""
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    text = message.split("\n")
    for x in range(len(text)):
        print(f"{start}{e_time}: {text[x]}")
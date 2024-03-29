import os, sys
import time

DEBUG = False
ERROR = True
INFO = True

def log(msg: str, type: str):
    path = os.path.join(os.path.dirname(__file__), "".join(os.path.basename(__file__).split(os.path.extsep)[:-1]) + "_data")
    os.makedirs(path, exist_ok=True)
    file = os.path.join(path, type + "s.log")
    with open(file, "a") as f:
        f.write(msg + "\n")
        f.close()

def debugger(message: str, objects=[], thread=None, use_time=True, short=False):
    global DEBUG
    if short:
        start = "[D]"
    else:
        start = "[DEBUG]"
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    if use_time:
        e_time = "[" + str(time.ctime()) + "]"
    else:
        e_time = ""
    msg = f"{start}{e_time}: " + message
    for x in range(len(objects)):
        _temp_type = type(objects[x])
        _temp_len = None
        try:
            _temp_len = len(objects[x])
        except:
            _temp_len = "<cannot calculate on unusual type>"
        _temp_content = objects[x]
        msg += f"\n{start}{e_time}: Object {x} type: {_temp_type}, len: {_temp_len}, contents: {_temp_content}"
    if DEBUG:
        print(msg)
    log(msg, "debug_log")

def exceptor(message: str, type=Exception, thread=None, short=False, use_time=False, exception_do=0):
    if short:
        start = "[E]"
    else:
        start = "[ERROR]"
    if use_time:
        e_time = "[" + str(time.ctime()) + "]"
    else:
        e_time = ""
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    if ERROR:
        print(f"{start}{e_time}[{str(type).upper()}]: {message}")
    log(f"{start}{e_time}[{str(type).upper()}]: {message}", "error")
    if exception_do == 0:
        sys.exit()
    if exception_do == 1:
        pass
    if exception_do == 2:
        raise type(message)
   

def info(message: str, thread=None, short=False, use_time=False):
    if short:
        start = "[I]"
    else:
        start = "[INFO]"
    if use_time:
        e_time = "[" + str(time.ctime()) + "]"
    else:
        e_time = ""
    if not thread == None:
        start += "[" + str(thread).upper() + "]"
    message.replace("\n", f"\n{start}{e_time}: ")
    if INFO:
        print(f"{start}{e_time}: {message}")
    log(f"{start}{e_time}: {message}", "info_log")
   
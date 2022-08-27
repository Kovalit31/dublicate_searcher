from ..plugins import collections
import os

def makedir(dir: str):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            return False
        except Exception as e:
            collections.exceptor(str(e),short=True, use_time=False, exception_do=1)
            return True
    else:
        return True

def get_line_from_file(file: str, line: int):
    data = " "
    with open(file) as opened_file:
        data = opened_file.readlines()[line].lstrip().rstrip()
        opened_file.close()
    return data

def strip_unneeded(string: str, what_strip: str):
    a = string.split(what_strip)
    return "".join(a)
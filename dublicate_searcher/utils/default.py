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

def get_line_from_file(file: str):
    data = " "
    with open(file) as opened_file:
        data = opened_file.readline().lstrip().rstrip()
        opened_file.close()
    return data

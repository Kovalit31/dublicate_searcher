import os
from . import *
from ..plugins import collections

PATH = os.path.dirname(__file__)

def makedir(dir2make: str) -> bool:
    if not os.path.exists(dir2make):
        os.makedirs(dir2make, exist_ok=True)
        return False
    else:
        return True

def get_line_from_file(file_path: str, line: int):
    data_from_line = " "
    with open(file_path) as opened_file:
        data_from_line = opened_file.readlines()[line].strip()
        opened_file.close()
    return data_from_line

def strip_unneeded(string: str, what_to_strip: str):
    temp = string.split(what_to_strip)
    return "".join(temp)

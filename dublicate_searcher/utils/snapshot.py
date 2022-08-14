import hashlib
import math
from ..plugins import collections

def get_hash_from_file(file: str):
    _hash = " "
    with open(file, "rb") as byte_file:
        _hash = hashlib.sha1(byte_file.read()).hexdigest()
        byte_file.close()
    return _hash

def get_bytes_from_file(file: str, byte_arr: list):
    return_arr = []
    with open(file, "rb") as byte_file:
        _file_length = len(bytearray(byte_file.read()))
        collections.debugger("In function _get_bytes_from_file: ", [_file_length, math.ceil(_file_length / 100), _file_length / 100], use_time=False)
        percent = math.ceil(_file_length / 100)
        percents_of_file = 1
        copy_arr = []
        for x in range(len(byte_arr)):
            copy_arr.append(byte_arr[x])
        total_need_to_get = percent * percents_of_file
        for x in range(total_need_to_get):
            pos_in_arr = 0
            if x < len(copy_arr):
                pos_in_arr = x
            else:
                pos_in_arr = x % len(copy_arr)
            while True:
                if copy_arr[pos_in_arr] > _file_length:
                    copy_arr[pos_in_arr] = math.ceil(copy_arr[pos_in_arr] / 2)
                else:
                    break
            byte_file.seek(copy_arr[pos_in_arr])
            return_arr.append(byte_file.read(1))
            copy_arr[pos_in_arr] *= 2
        byte_file.close()
    return return_arr
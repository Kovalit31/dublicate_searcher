import hashlib
import math
from copy import deepcopy
from ..plugins import collections

def get_hash_from_file(file_path: str) -> str:
    file_hashsum = " "
    with open(file_path, "rb") as opened_byte_file:
        file_hashsum = hashlib.sha1(opened_byte_file.read()).hexdigest()
        opened_byte_file.close()
    return file_hashsum

def get_bytes_from_file(file_path: str, byte_arr: list) -> list:
    return_arr = []
    with open(file_path, "rb") as opened_byte_file:
        opened_file_length = len(bytearray(opened_byte_file.read()))
        collections.debugger("In function _get_bytes_from_file: ", [opened_file_length, math.ceil(opened_file_length / 100), opened_file_length / 100], use_time=False)
        one_percent_of_file = math.ceil(opened_file_length / 100)
        percents_of_file_need = 1
        byte_arr_copy = deepcopy(byte_arr)
        total_need_to_get_bytes = one_percent_of_file * percents_of_file_need
        for getting_byte in range(total_need_to_get_bytes):
            position_in_arr = 0
            if getting_byte < len(byte_arr_copy):
                position_in_arr = getting_byte
            else:
                position_in_arr = getting_byte % len(byte_arr_copy)
            while True:
                if byte_arr_copy[position_in_arr] > opened_file_length:
                    byte_arr_copy[position_in_arr] = math.ceil(byte_arr_copy[position_in_arr] / 2)
                    if byte_arr_copy[position_in_arr] == opened_file_length:
                        byte_arr_copy[position_in_arr] -= 1
                else:
                    break
            opened_byte_file.seek(byte_arr_copy[position_in_arr])
            return_arr.append(opened_byte_file.read(1))
            byte_arr_copy[position_in_arr] *= 2
        opened_byte_file.close()
    return return_arr
#!/usr/bin/env python3.9
from copy import deepcopy
import hashlib
import math
import os
import sys
import uuid

from .plugins import collections, config
from .utils import cacher, paths, snapshot, default


def _check_consistent(filename: str, byte_file: str, hash_file: str, byte_arr: list):
    try:
        check_hash = 0
        hash_cached = " "
        hash_real = " "
        byte_array_cached = []
        byte_array_real = []
        byte_array_real = snapshot.get_bytes_from_file(filename, byte_arr)
        with open(byte_file, "rb") as f:
            _bytes = f.read()
            for x in range(len(_bytes)):
                byte_array_cached.append(_bytes[x])
            f.close()
        if len(byte_array_cached) == len(byte_array_real):
            for x in range(len(byte_array_real)):
                if byte_array_real[x] == byte_array_cached[x]:
                    pass
                else:
                    return False
            else:
                return True
        else:
            check_hash = 1
        if check_hash:
            with open(hash_file) as f:
                hash_cached = f.readline().rstrip().lstrip()
                f.close()
            hash_real = snapshot.get_hash_from_file(filename)
            if hash_cached.lstrip().rstrip().lower() == hash_real.lstrip().rstrip().lower():
                return True
            else:
                return False
    except:
        return False

def main(_path):
    metadir = paths.DEFAULT_CACHE_META_DIR
    bitsdir = paths.DEFAULT_CACHE_COPY_DIR
    hashdir = paths.DEFAULT_CACHE_HASH_DIR
    cached = []
    byte_arr = [73, 76, 485, 35, 456]
    for root, dirs, files in os.walk(_path):
        collections.debugger("In main: ", [root, files], use_time=False)
        for x in range(len(files)):
            cur_file = os.path.join(root, files[x])
            collections.debugger("Current file:", [cur_file], use_time=False)
            found, data = cacher.find_in_cache(cur_file)
            if found:
                consistent = _check_consistent(cur_file, data[2], data[1], byte_arr)
                if consistent:
                    cached.append(cur_file)
                else:
                    cacher.del_from_cache(data[3])
                    cacher.add_to_cache(cur_file, byte_arr)
                    cached.append(cur_file)
            else:
                cacher.add_to_cache(cur_file, byte_arr)
                cached.append(cur_file)
    dublicates = []
    filtered = deepcopy(cached)
    appromated = len(cached)
    while x < appromated:
        selected = filtered[0]
        other = deepcopy(filtered[1:])
        booled, arr = cacher.find_in_cache(selected)
        if booled:
            hashsum = default.get_line_from_file(arr[1]).lower()
        else:
            cacher.del_from_cache(selected)
            cacher.add_to_cache(selected, byte_arr)
            booled, arr = cacher.find_in_cache(selected)
            if not booled:
                collections.exceptor("Cannot determine a file rewriting!", short=True, exception_do=2)
        dublicates_for_this = []
        for y in range(len(other)):
            other_bool, other_data = cacher.find_in_cache(other[y])
            other_hashsum = default.get_line_from_file(other_data[1]).lower()
            if hashsum == other_hashsum:
                dublicates_for_this.append(other_data[0])
        dublicates.append(deepcopy(dublicates_for_this))
        for x in range(len(dublicates_for_this)):
            f = filtered.index(dublicates_for_this[x])
            filtered.pop(f)
        appromated -= len(dublicates_for_this)
        x += 1
    for x in range(len(dublicates)):
        collections.info(f"Dublicates of file '{dublicates[x][0]}': \n{dublicates[x][1:]}", short=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        a = input("Path to work:")
    else:
        a = sys.argv[1]
    _path = os.path.realpath(a)
    main(_path)

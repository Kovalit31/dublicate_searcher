#!/usr/bin/env python3.9
from copy import deepcopy
import os
import sys

from .plugins import collections, config
from .utils import cacher, paths, snapshot, default


def _check_consistent(filename: str, _uuid: str, byte_arr: list):
    try:
        exist, data = cacher.get_cache_data_by_uuid(_uuid)
        if exist:
            hash_file, byte_file = data
        else:
            collections.exceptor(f"No found file with this uuid {_uuid}!", short=True)
        check_hash = 0
        hash_cached = " "
        hash_real = " "
        byte_array_cached = []
        byte_array_real = snapshot.get_bytes_from_file(filename, byte_arr)
        collections.debugger(f"Getting bytes from file: {byte_file}", use_time=False, short=True)
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
            collections.debugger(f"Checking hash, because bits is broken: {hash_file}", use_time=False, short=True)
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
    uuids = []
    byte_arr = [73, 76, 485, 35, 456]
    
    for root, dirs, files in os.walk(_path):
        collections.debugger("In main: ", [root, files], use_time=False)
        for x in range(len(files)):
            cached.append(os.path.join(root, files[x]))

    collections.debugger("Working on cache!", use_time=False, short=True)
    for x in range(len(cached)):
        tryings = 0
        try:
            collections.debugger(f"Trying: ", [tryings], use_time=False, short=True)
            collections.debugger("Finding file: ", [cached[x]], use_time=False, short=True)
            exist, _uuid = cacher.find_in_cache(cached[x])
            consistent = False
            if exist:
                collections.debugger("It exist", use_time=False, short=True)
                if _check_consistent(cached[x], _uuid, byte_arr):
                    collections.debugger("It good", use_time=False, short=True)
                    uuids.append(_uuid)
                else:
                    collections.debugger("It bad", use_time=False, short=True)
                    consistent = False
            else:
                collections.debugger("It not exist", use_time=False, short=True)
                consistent = False
            if not consistent:
                collections.debugger("Deleting it!", use_time=False, short=True)
                cacher.del_from_cache(_uuid)
                collections.debugger(f"Adding it with args: {cached[x]}, {byte_arr}", use_time=False, short=True) 
                _uuid = cacher.add_to_cache(cached[x], byte_arr)
                tryings += 1
        except Exception as e:
            collections.exceptor(f"Cannot setup cache: {str(e)}", type=NotImplementedError, short=True, exception_do=2)
    
    dublicates = []
    filtered = deepcopy(uuids)
    while len(filtered) > 0:
        selected = filtered[0]
        collections.debugger(f"Selected uuid: {selected}", use_time=False, short=True)
        other = deepcopy(filtered[1:])
        arr = cacher.get_cache_data_by_uuid(selected)
        collections.debugger(f"It data: {arr}", use_time=False, short=True)
        hashsum = default.get_line_from_file(arr[0]).lower()
        dublicates_for_this = []
        for y in range(len(other)):
            other_arr = cacher.get_cache_data_by_uuid(other[y])
            other_hashsum = default.get_line_from_file(other_arr[0]).lower()
            if hashsum == other_hashsum:
                collections.debugger(f"Is dublicate with uuid: {other_arr[0]}\nFilename: {cacher.get_cache_name_by_uuid(other_arr[0])}", use_time=False, short=True)
                dublicates_for_this.append(cacher.get_cache_name_by_uuid(other_arr[0]))
        dublicates.append(deepcopy(dublicates_for_this))
        for x in range(len(dublicates_for_this)):
            f = filtered.index(dublicates_for_this[x])
            collections.debugger(f"Deleting uuid from filter: {dublicates_for_this[x]}", use_time=False, short=True)
            filtered.pop(f)
    for x in range(len(dublicates)):
        collections.info(f"Dublicates of file '{dublicates[x][0]}': \n{dublicates[x][1:]}", short=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        a = input("Path to work:")
    else:
        a = sys.argv[1]
    _path = os.path.realpath(a)
    main(_path)

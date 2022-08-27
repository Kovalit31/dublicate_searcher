#!/usr/bin/env python3.9
from copy import deepcopy
import os
import sys

from .plugins import collections, config
from .utils import cacher, paths, snapshot, default


def _check_consistent(_uuid: str, byte_arr: list):
    try:
        exist, data = cacher.get_cache_data_by_uuid(_uuid)
        if exist:
            hash_cached, byte_file = data
        else:
            collections.exceptor(f"No found file with this uuid {_uuid}!", short=True)
        check_hash = 0
        file = cacher.get_cache_name_by_uuid(_uuid)
        hash_real = " "
        byte_array_cached = []
        byte_array_real = snapshot.get_bytes_from_file(file, byte_arr)
        collections.debugger(f"Getting bytes from file: {byte_file}", use_time=False, short=True)
        with open(byte_file, "rb") as f:
            _bytes = f.read()
            for x in range(len(_bytes)):
                byte_array_cached.append(_bytes[x])
            f.close()
        if len(byte_array_cached) == len(byte_array_real):
            for x in range(len(byte_array_real)):
                if not byte_array_real[x] == byte_array_cached[x]:
                    check_hash = 1
                    break
            else:
                return True
        else:
            check_hash = 1
        if check_hash:
            collections.debugger(f"Checking hash, because bits is broken: {file}", use_time=False, short=True)
            hash_real = snapshot.get_hash_from_file(file)
            if hash_cached.lstrip().rstrip().lower() == hash_real.lstrip().rstrip().lower():
                return True
            else:
                return False
    except:
        return False

def main(_path):
    cached = []
    uuids = []
    byte_arr = [73, 76, 485, 35, 456]
    for root, dirs, files in os.walk(_path):
        collections.debugger("In main: ", [root, files], use_time=False)
        for x in range(len(files)):
            cached.append(os.path.join(root, files[x]))
    estimated = len(cached)
    processed = 0
    collections.info("It was caching and, if need, fixing cache...", short=True)
    collections.debugger("Working on cache!", use_time=False, short=True)
    for x in range(len(cached)):
        try:
            collections.info(f"Processed {processed} from {estimated}...", short=True)
            collections.debugger("Finding file: ", [cached[x]], use_time=False, short=True)
            exist, _uuid = cacher.find_in_cache(cached[x])
            consistent = False
            if exist:
                collections.debugger("It exist", use_time=False, short=True)
                if _check_consistent(_uuid, byte_arr):
                    collections.debugger("It good", use_time=False, short=True)
                    consistent = True
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
            uuids.append(_uuid)
            processed += 1
        except Exception as e:
            collections.exceptor(f"Cannot setup cache: {str(e)}", type=NotImplementedError, short=True, exception_do=2)
    
    dublicates = []
    filtered = deepcopy(uuids)
    est = len(filtered)
    did = 0
    collections.info("It was finding dublicates...")
    while len(filtered) > 0:
        collections.info(f"Processed {did} from {est}...", short=True)
        selected = filtered[0]
        collections.debugger(f"Selected uuid: {selected}", use_time=False, short=True)
        other = deepcopy(filtered[0:])
        exist, arr = cacher.get_cache_data_by_uuid(selected)
        hashsum = arr[0]
        collections.debugger("It's data: ", [exist, arr, hashsum])
        dublicates_for_this = []
        collections.debugger("Arrays initialized: ", [filtered, other])
        for y in range(len(other)):
            exist_other, other_arr = cacher.get_cache_data_by_uuid(other[y])
            other_hashsum = other_arr[0]
            collections.debugger("Getting other uuid data: ", [exist_other, other_arr, other_hashsum])
            if hashsum == other_hashsum:
                collections.debugger(f"Is dublicate with uuid: {other[y]}\nFilename: {cacher.get_cache_name_by_uuid(other[y])}", use_time=False, short=True)
                dublicates_for_this.append(other[y])
        dublicates.append(deepcopy(dublicates_for_this))
        for x in range(len(dublicates_for_this)):
            did += 1
            f = filtered.index(dublicates_for_this[x])
            collections.debugger(f"Deleting uuid from filter: {dublicates_for_this[x]}", use_time=False, short=True)
            filtered.pop(f)
    array_humaned = []
    for x in range(len(dublicates)):
        array_humaned.append([])
        for y in range(len(dublicates[x])):
            array_humaned[x].append(cacher.get_cache_name_by_uuid(dublicates[x][y]))
    for x in range(len(array_humaned)):
        collections.info(f"Dublicates for file {array_humaned[x][0]}: {array_humaned[x][1:]}", short=True)
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        a = input("Path to work:")
    else:
        a = sys.argv[1]
    _path = os.path.realpath(a)
    main(_path)

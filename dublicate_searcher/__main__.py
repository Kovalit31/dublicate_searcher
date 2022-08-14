#!/usr/bin/env python3.9
import hashlib
import os
import sys
import uuid
import math

from .utils import hash, config, collections
from .utils.config_data import default

def _get_bytes_from_file(file: str, byte_arr: list):
    ret = []
    with open(file, "rb") as d:
        _length = len(bytearray(d.read()))
        percent = math.floor(_length // 100)
        percent_of_file = 1
        new_arr = []
        for x in range(len(byte_arr)):
            new_arr.append(byte_arr[x])
        for x in range(percent * percent_of_file):
            y = x % len(new_arr)
            while True:
                if new_arr[y] > _length:
                    if len(new_arr)-1 > y:
                        if y > 0:
                            y -= 1
                        else:
                            y = 0
                    else:
                        y = len(new_arr) - 1
                break
            try:
                d.seek(new_arr[y])
                ret.append(d.read(1))
                new_arr[y] *= 2
            except Exception as e:
                collections.debugger("Raised: " + str(e))
                break
        d.close()
    return ret

def _get_hash_from_file(file: str):
    _hash = " "
    with open(file, "rb") as d:
        _hash = hashlib.sha1(d.read()).hexdigest()
        d.close()
    return _hash


def _write_prepare(string: str):
    pass

def _makedir(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            return False
        except Exception as e:
            collections.debugger(str(e))
            return True
    else:
        return True

def _search_file_in_cache(file: str):
    metadir = default.DEFAULT_CACHE_META_DIR
    bitsdir = default.DEFAULT_CACHE_COPY_DIR
    hashdir = default.DEFAULT_CACHE_HASH_DIR
    _makedir(metadir)
    _makedir(bitsdir)
    _makedir(hashdir)
    try:
        meta_objects = os.listdir(metadir)
        for x in range(len(meta_objects)):
            temp_files = os.listdir(os.path.join(metadir, meta_objects[x]))
            for y in range(len(temp_files)):
                #collections.debugger(f"Working on '{meta_objects[x] + temp_files[y]}'")
                name = " "
                hashsum = " "
                bitsfile = " "
                if_found = 0
                with open(os.path.join(metadir, meta_objects[x], temp_files[y], "filename")) as f:
                    name = f.readline()
                    name.lstrip().rstrip()
                    #collections.debugger(f"Found filename '{name}'")
                    if name == file:
                        #collections.debugger(f"FOUND file '{file}'")
                        if_found = 1
                    f.close()
                if if_found:
                    #collections.debugger("Prepare to check hashsum, if bits will not examing...")
                    with open(os.path.join(metadir, meta_objects[x], temp_files[y], "hashsum")) as f:
                        hashsum = f.readline().rstrip().lstrip().lower()
                        f.close()
                    #collections.debugger("Examing bits file...")
                    with open(os.path.join(metadir, meta_objects[x], temp_files[y], "bitsfile")) as f:
                        bitsfile = f.readline().rstrip().lstrip()
                        f.close()
                    returning = []
                    returning.append(name)
                    returning.append(hashsum)
                    returning.append(bitsfile)
                    returning.append(meta_objects[x] + temp_files[y])
                    return True, returning
        else:
            return False, []
    except Exception as e:
        collections.debugger("Cannot do latest job, because raised: " + str(e))
        return False, []

def _work_with_file__uuid_dir(path: str, create_subfolder=True):
    uid = " "
    while True:
        _uuid = uuid.uuid4()
        uid = str(_uuid)
        if _makedir(os.path.join(path, uid[:2])):
            if create_subfolder:
                if _makedir(os.path.join(path, uid[:2], uid[2:])):
                    pass
                else:
                    break
            else:
                if os.path.exists(os.path.join(path, uid[:2], uid[2:])):
                    pass
                else:
                    break
    return uid

def _work_with_file(file: str, byte_arr: list):
    uid = _work_with_file__uuid_dir(default.DEFAULT_CACHE_META_DIR)
    collections.debugger("Creating 'filename' structure...")
    with open(os.path.join(default.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "filename"), "x") as f:
        f.write(file)
        f.close()
    huid = _work_with_file__uuid_dir(default.DEFAULT_CACHE_HASH_DIR, create_subfolder=False)
    collections.debugger("Creating 'hashsum' structure...")
    with open(os.path.join(default.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "hashsum"), "x") as f:
        f.write(os.path.join(default.DEFAULT_CACHE_HASH_DIR, huid[:2], huid[2:]))
        f.close()
    with open(os.path.join(default.DEFAULT_CACHE_HASH_DIR, huid[:2], huid[2:]), "x") as f:
        f.write(_get_hash_from_file(file))
        f.close()
    buid = _work_with_file__uuid_dir(default.DEFAULT_CACHE_COPY_DIR, create_subfolder=False)
    collections.debugger("Creating 'bitsfile' structure...")
    with open(os.path.join(default.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "bitsfile"), "x") as f:
        f.write(os.path.join(default.DEFAULT_CACHE_COPY_DIR, buid[:2], buid[2:]))
        f.close()
    with open(os.path.join(default.DEFAULT_CACHE_COPY_DIR, buid[:2], buid[2:]), "xb") as f:
        ret = _get_bytes_from_file(file, byte_arr)
        for x in range(len(ret)):
            f.write(ret[x])
        f.close()

def _del_from_cache(file_uuid: str):
    pass

def _check_consistent(filename: str, byte_file: str, hash_file: str, byte_arr: list):
    check_hash = 0
    hash_cached = " "
    hash_real = " "
    byte_array_cached = []
    byte_array_real = []
    byte_array_real = _get_bytes_from_file(filename, byte_arr)
    with open(byte_file, "rb") as f:
        _bytes = f.read()
        for x in range(len(_bytes)):
            byte_array_cached.append(_bytes[x])
        f.close()
    if len(byte_array_cached) == len(byte_array_real):
        return True
    else:
        check_hash = 1
    if check_hash:
        with open(hash_file) as f:
            hash_cached = f.readline().rstrip().lstrip()
            f.close()
        hash_real = _get_hash_from_file(filename)
        if hash_cached.lstrip().rstrip().lower() == hash_real.lstrip().rstrip().lower():
            return True
        else:
            return False


def main(_path):
    metadir = default.DEFAULT_CACHE_META_DIR
    bitsdir = default.DEFAULT_CACHE_COPY_DIR
    hashdir = default.DEFAULT_CACHE_HASH_DIR
    cached = []
    byte_arr = [73, 76, 485, 35, 456]
    for root, dirs, files in os.walk(_path):
        #print(root, dirs, files)
        for x in range(len(files)):
            cur_file = os.path.join(root, files[x])
            print(cur_file)
            found, data = _search_file_in_cache(cur_file)
            if found:
                consistent = _check_consistent(data[0], data[2], data[1], byte_arr)
                if consistent:
                    pass
                else:
                    _del_from_cache(data[3])
                    _work_with_file(cur_file, byte_arr)
            else:
                _work_with_file(cur_file, byte_arr)
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        a = input("Path to work:")
    else:
        a = sys.argv[1]
    _path = os.path.realpath(a)
    main(_path)

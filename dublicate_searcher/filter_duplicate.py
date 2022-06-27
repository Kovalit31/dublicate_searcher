#!/usr/bin/env python3.9
import os
import hashlib
from concurrent.futures.thread import ThreadPoolExecutor

dublicate = []
cpu = 2

def get_hash(ffile):
    with open(ffile, "rb") as file:
        hash = hashlib.sha1(file.read()).hexdigest()
        file.close()
    return hash

def files_from_dir(_dir):
    content = os.listdir(_dir)
    files = []
    for x in content:
        if os.path.isfile(os.path.join(_dir, x)):
            files.append(x)
    return files

def hash_checker(hash, ffile, orig):
    # print("File: '", orig,"'\n","Checking for duplicate: '" ,ffile, "'\n", sep='')
    if hash == get_hash(ffile):
        print(f"File '{ffile}' is equal to original file '{orig}'")
        global dublicate
        dublicate.append(ffile)


def create_dir(_dir):
        try:
            os.mkdir(_dir)
        except:
            if os.path.exists(_dir) and os.path.isdir(_dir):
                pass
            elif not os.path.isdir(_dir):
                try:
                    dst = _dir
                    while True:
                        if os.path.exists(dst):
                            dst += ".old"
                        else:
                            break
                    os.rename(_dir, dst=dst)
                    os.mkdir(_dir)
                except:
                    raise Exception("Your partition is full and/or read-only")
            else:
                raise Exception("Your partition is full and/or read-only")

def main(_path):
    global dublicate
    _build = os.path.join(_path, "_build")
    _files = files_from_dir(_path)
    _temp = os.path.join(_path, "_temp")
    create_dir(_temp)
    global cpu
    # print(_files, _build)
    try:
        while True:
            ffile = os.path.join(_path, _files[0])
            move_build = os.path.join(_build, _files[0])
            print(ffile, move_build)
            hash = get_hash(ffile)
            _temp_files = _files
            _temp_files.pop(0)
            # print(_temp_files)
            with ThreadPoolExecutor(max_workers=cpu*4) as executor:
                for x in range(len(_temp_files)):
                    # print(_temp_files[x], x)
                    _tempf = os.path.join(_path, _temp_files[x])
                    executor.submit(hash_checker, hash, _tempf, ffile)
            if len(dublicate) > 0:
                for x in range(len(dublicate)):
                    src = os.path.join(_path, dublicate[x])
                    dst = os.path.join(_build, dublicate[x])
                    os.rename(src, dst)
            src = os.path.join(_path, ffile)
            dst = os.path.join(_temp, ffile)
            os.rename(src, dst)
            _files = files_from_dir(_path)
    except KeyboardInterrupt or EOFError:
        _ = os.listdir(_temp)
        for x in range(len(_)):
            dst = os.path.join(_path, _[x])
            src = os.path.join(_temp, _[x])
            os.rename(src, dst)
    print(dublicate)

if __name__ == "__main__":
    a = input("Path to work:")
    _path = os.path.realpath(a)
    main(_path)
import os
import uuid
import pathlib

from ..plugins import collections
from . import default, paths, snapshot


def _uuids_in_cache(section: str):
    collections.debugger(f"Getting used uuids", use_time=False, short=True)
    firsts = os.listdir(section)
    returning = []
    for x in range(len(firsts)):
        seconds = os.listdir(os.path.join(section, firsts[x]))
        for y in range(len(seconds)):
            returning.append(firsts[x] + seconds[y])
    return returning

def _add_to_cache__gen_uuid(path: str):
    collections.debugger(f"Generating uuid", use_time=False, short=True)
    while True:
        _uuid = default.strip_unneeded(str(uuid.uuid4()) + str(uuid.uuid4()), "-")
        if not _uuid in _uuids_in_cache(path):
            break
        else:
            pass
    return _uuid

def _add_to_cache__create_file(path: str):
    try:
        filename = pathlib.Path(path)
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.touch(exist_ok=True)
        return filename
    except:
        return False

def add_to_cache(file: str, byte_arr: list): # BUG: files is creating randomly!
    uid = _add_to_cache__gen_uuid(paths.DEFAULT_CACHE_META_DIR)
    collections.debugger(f"Creating 'filename' structure with uuid {uid}...", use_time=False)
    filename = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "filename"))
    while True:
        with open(filename, "w+") as opened:
            opened.write(file)
            opened.close()
        if filename.exists():
            break
    huid = _add_to_cache__gen_uuid(paths.DEFAULT_CACHE_HASH_DIR)
    collections.debugger("Creating 'hashsum' structure...", use_time=False)
    collections.debugger("Step 1: creating data in meta dir..")
    hashfile_info = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "hashfile"))
    hashfile = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_HASH_DIR, huid[:2], huid[2:]))
    while True:
        with open(hashfile_info, "w+") as opened:
            opened.write(huid)
            opened.close()
        if hashfile_info.exists():
            break
    collections.debugger("Step 2: creating data in hash dir..")
    while True:
        with open(hashfile, "w+") as opened:
            opened.write(snapshot.get_hash_from_file(file))
            opened.close()
        if os.path.exists(hashfile):
            break
    buid = _add_to_cache__gen_uuid(paths.DEFAULT_CACHE_COPY_DIR)
    collections.debugger("Creating 'bitsfile' structure...", use_time=False)
    collections.debugger("Step 1: creating data in meta dir..")
    bits_info = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "bitsfile"))
    bits =  _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_COPY_DIR, buid[:2], buid[2:]))
    while True:
        with open(bits_info, "w+") as opened:
            opened.write(buid)
            opened.close()
        if os.path.exists(bits_info):
            break
    collections.debugger("Step 2: creating data in bits dir..")
    while True:
        with open(bits, "wb+") as byte_opened:
            ret = snapshot.get_bytes_from_file(file, byte_arr)
            for x in range(len(ret)):
                byte_opened.write(ret[x])
            byte_opened.close()
        if os.path.exists(bits):
            break
    return uid
        
def del_from_cache(file_uuid: str):
    try:
        collections.debugger(f"It's deleting uuid: {file_uuid}", use_time=False, short=True)
        path = paths.DEFAULT_CACHE_META_DIR
        first_dir = file_uuid[:2]
        second_dir = file_uuid[2:]
        hashsum_file = os.path.normpath(default.get_line_from_file(os.path.join(path, first_dir, second_dir, "hashfile")))
        bits_file = os.path.normpath(default.get_line_from_file(os.path.join(path, first_dir, second_dir, "bitsfile")))
        os.remove(os.path.join(path, first_dir, second_dir, "bitsfile"))
        os.remove(os.path.join(path, first_dir, second_dir, "hashfile"))
        os.remove(os.path.join(paths.DEFAULT_CACHE_HASH_DIR, hashsum_file[:2], hashsum_file[2:]))
        os.remove(os.path.join(paths.DEFAULT_CACHE_COPY_DIR, bits_file[:2], bits_file[2:]))
        os.remove(os.path.join(path, first_dir, second_dir, "filename"))
        os.rmdir(os.path.join(path, first_dir, second_dir))
        cache = os.listdir(os.path.join(path, first_dir))
        if len(cache) == 0:
            os.rmdir(os.path.join(path, first_dir))
        return True
    except Exception as e:
        collections.exceptor("Excepted deleting, because " + str(e), short=True, exception_do=1)
        return False
    

def find_in_cache(file: str):
    metadir = paths.DEFAULT_CACHE_META_DIR
    bitsdir = paths.DEFAULT_CACHE_COPY_DIR
    hashdir = paths.DEFAULT_CACHE_HASH_DIR
    default.makedir(metadir)
    default.makedir(bitsdir)
    default.makedir(hashdir)
    try:
        meta_objects = os.listdir(metadir)
        for x in range(len(meta_objects)):
            temp_files = os.listdir(os.path.join(metadir, meta_objects[x]))
            collections.debugger("First and second dirs in meta: ", [meta_objects, temp_files, x])
            for y in range(len(temp_files)):
                collections.debugger(f"Working on '{meta_objects[x] + temp_files[y]}'", use_time=False)
                name = " "
                if_found = 0
                try:
                    with open(os.path.join(metadir, meta_objects[x], temp_files[y], "filename")) as f:
                        name = f.readline().lstrip().rstrip()
                        f.close()
                        collections.debugger(f"Found filename '{name}'", use_time=False)
                except:
                    collections.debugger(f"File with uuid '{meta_objects[x] + temp_files[y]}' not found in cache!", short=True, use_time=False)
                    
                if name == file:
                    collections.debugger(f"FOUND file '{file}'", use_time=False)
                    if_found = 1
                if if_found:
                    return True, meta_objects[x] + temp_files[y]
        else:
            return False, None
    except Exception as e:
        collections.exceptor("Cannot do latest job, because raised: " + str(e), short=True, exception_do=1)
        return False, meta_objects[x] + temp_files[y]

def get_cache_data_by_uuid(file_uuid: str):
    try:
        _temp = " "
        hashfile = " "
        bitsfile = " "
        collections.debugger("Getting up 'hashsum'")
        with open(os.path.join(paths.DEFAULT_CACHE_META_DIR, file_uuid[:2], file_uuid[2:], "hashsum")) as file:
            _temp = file.readline().rstrip().lstrip()
            file.close()
        hashfile = os.path.join(paths.DEFAULT_CACHE_HASH_DIR, _temp[:2], _temp[2:])
        collections.debugger("Getting up bits file...")
        with open(os.path.join(paths.DEFAULT_CACHE_META_DIR, file_uuid[:2], file_uuid[2:], "bitsfile")) as file:
            _temp = file.readline().rstrip().lstrip()
            file.close()
        bitsfile = os.path.join(paths.DEFAULT_CACHE_COPY_DIR, _temp[:2], _temp[2:])
        returning = []
        returning.append(hashfile)
        returning.append(bitsfile)
        return True, returning
    except Exception as e:
        collections.exceptor("Problem to get data: " + str(e), short=True, exception_do=1)
        return False, []
    
def get_cache_name_by_uuid(_uuid: str):
    collections.debugger(f"Getting name by uuid: {_uuid}", use_time=False, short=True)
    path = os.path.join(paths.DEFAULT_CACHE_META_DIR, _uuid[:2], _uuid[2:], "filename")
    returned = " "
    with open(path) as file:
        returned = file.readline().lstrip().rstrip()
        file.close()
    return returned
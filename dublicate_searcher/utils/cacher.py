import os
import uuid
import pathlib

from ..plugins import collections
from . import paths, snapshot, hash, strip_unneeded, makedir, get_line_from_file

def create_cache_dirs() -> list:
    metadir = paths.DEFAULT_CACHE_META_DIR
    bytesdir = paths.DEFAULT_CACHE_COPY_DIR
    makedir(metadir)
    makedir(bytesdir)
    return_arr = []
    return_arr.append(metadir)
    return_arr.append(bytesdir)
    return return_arr

def _uuids_in_cache(section: str) -> list:
    collections.debugger(f"Getting used uuids", use_time=False, short=True)
    firsts_symbols = os.listdir(section)
    return_arr = []
    for x in range(len(firsts_symbols)):
        seconds_symbols = os.listdir(os.path.join(section, firsts_symbols[x]))
        for y in range(len(seconds_symbols)):
            return_arr.append(firsts_symbols[x] + seconds_symbols[y])
    return return_arr

def _add_to_cache__gen_uuid(path: str) -> str:
    collections.debugger(f"Generating uuid", use_time=False, short=True)
    while True:
        _uuid = strip_unneeded(str(uuid.uuid4()) + str(uuid.uuid4()), "-")
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

def _add_to_cache__as_hashsum(file_path: str, section_path: str):
    available_shas = hash.get_sha_v1_avialables()
    for x in range(len(available_shas)):
        path_hashsum = hash.get_sha(file_path.encode("utf-8"), sha_len=available_shas[x])
        if not path_hashsum in _uuids_in_cache(section_path):
            return path_hashsum
    else:
        raise NotImplementedError("Cannot do a unusual hashsum, because all hashsums is already containing!")
        

def add_to_cache(file_path_for_caching: str, byte_arr: list) -> str:
    meta_uuid = _add_to_cache__as_hashsum(file_path_for_caching, paths.DEFAULT_CACHE_META_DIR)
    bytes_uuid = _add_to_cache__gen_uuid(paths.DEFAULT_CACHE_COPY_DIR)
    collections.debugger(f"Creating meta structure with uuid {meta_uuid}...", use_time=False)
    meta_file = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, meta_uuid[:2], meta_uuid[2:]))
    while True:
        lines2write = []
        lines2write.append(file_path_for_caching)
        lines2write.append(snapshot.get_hash_from_file(file_path_for_caching))
        lines2write.append(bytes_uuid)
        with open(meta_file, "w+") as opened_file:
            for x in range(len(lines2write)):
                opened_file.write(lines2write[x] + "\n")
            opened_file.close()
        if meta_file.exists():
            break
    bytes_file = _add_to_cache__create_file(os.path.join(paths.DEFAULT_CACHE_COPY_DIR, bytes_uuid[:2], bytes_uuid[2:]))
    collections.debugger("Creating data in bits dir..")
    while True:
        with open(bytes_file, "wb+") as opened_bytes_file:
            byte_arr2write = snapshot.get_bytes_from_file(file_path_for_caching, byte_arr)
            for x in range(len(byte_arr2write)):
                opened_bytes_file.write(byte_arr2write[x])
            opened_bytes_file.close()
        if os.path.exists(bytes_file):
            break
    return meta_uuid

def del_from_cache(cached_file_uuid: str) -> bool:
    try:
        collections.debugger(f"It's deleting uuid: {cached_file_uuid}", use_time=False, short=True)
        firsts_symbols = cached_file_uuid[:2]
        seconds_symbols = cached_file_uuid[2:]
        bytes_file_uuid = os.path.join(get_line_from_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, firsts_symbols, seconds_symbols), 2))
        os.remove(os.path.join(paths.DEFAULT_CACHE_COPY_DIR, bytes_file_uuid[:2], bytes_file_uuid[2:]))
        os.remove(os.path.join(paths.DEFAULT_CACHE_META_DIR, firsts_symbols, seconds_symbols))
        cache = os.listdir(os.path.join(paths.DEFAULT_CACHE_META_DIR, firsts_symbols))
        if len(cache) == 0:
            os.rmdir(os.path.join(paths.DEFAULT_CACHE_META_DIR, firsts_symbols))
        return True
    except Exception as e:
        collections.exceptor("Excepted deleting, because " + str(e), short=True, exception_do=1)
        return False
    

def find_in_cache(file_path: str):
    metadir, no_req = create_cache_dirs()
    try:
        available_shas = hash.get_sha_v1_avialables()
        for x in range(len(available_shas)):
            path_hashsum = hash.get_sha(file_path.encode("utf-8"), sha_len=available_shas[x])
            try:
                cached_path = get_line_from_file(os.path.join(metadir, path_hashsum[:2], path_hashsum[2:]), 0)
            except:
                cached_path = " "
            if cached_path == file_path:
                return True, path_hashsum
        else:
            return False, None
    except Exception as e:
        collections.exceptor("Cannot do latest job, because raised: " + str(e), short=True, exception_do=1)
        return False, None

def get_cached_data_by_uuid(cached_file_uuid: str):
    # try:
        bytes_file_uuid = " "
        cached_file_hashsum = " "
        bytes_file_path = " "
        collections.debugger("Getting up 'hashsum'")
        _temp = []
        with open(os.path.join(paths.DEFAULT_CACHE_META_DIR, cached_file_uuid[:2], cached_file_uuid[2:])) as f: # Interpreter do error here: TypeError: 'int' object isnot subscriptable
            _temp = f.readlines()
            f.close()
        cached_file_hashsum = _temp[1].strip()
        # cached_file_hashsum = get_line_from_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, cached_file_uuid[:2], cached_file_uuid[2:]), 1)
        bytes_file_uuid = get_line_from_file(os.path.join(paths.DEFAULT_CACHE_META_DIR, cached_file_uuid[:2], cached_file_uuid[2:]), 2)
        bytes_file_path = os.path.join(paths.DEFAULT_CACHE_COPY_DIR, bytes_file_uuid[:2], bytes_file_uuid[2:])
        return_arr = []
        return_arr.append(cached_file_hashsum)
        return_arr.append(bytes_file_path)
        return True, return_arr
    # except Exception as e:
    #     collections.exceptor("Problem to get data: " + str(e), short=True, exception_do=1)
    #     return False, []
    
def get_cached_path_by_uuid(cached_file_uuid: str) -> str:
    collections.debugger(f"Getting name by uuid: {cached_file_uuid}", use_time=False, short=True)
    cached_meta_path = os.path.join(paths.DEFAULT_CACHE_META_DIR, cached_file_uuid[:2], cached_file_uuid[2:])
    return_arr = get_line_from_file(cached_meta_path, 0)
    return return_arr
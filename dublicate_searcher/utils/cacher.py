import os
import uuid

from ..plugins import collections
from . import default, paths, snapshot


def _add_to_cache__uuid_dir(path: str, create_subfolder=True):
    uid = " "
    while True:
        _uuid = uuid.uuid4()
        uid = str(_uuid)
        if default.makedir(os.path.join(path, uid[:2])):
            if create_subfolder:
                if default.makedir(os.path.join(path, uid[:2], uid[2:])):
                    pass
                else:
                    break
            else:
                if os.path.exists(os.path.join(path, uid[:2], uid[2:])):
                    pass
                else:
                    break
    return uid

def _add_to_cache__writer(file: str, what: str):
    with open(file, "x") as f:
        f.write(what)
        f.close()

def add_to_cache(file: str, byte_arr: list):
    uid = _add_to_cache__uuid_dir(paths.DEFAULT_CACHE_META_DIR)
    collections.debugger(f"Creating 'filename' structure with uuid {uid}...", use_time=False)
    _add_to_cache__writer(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "filename"), file)
    huid = _add_to_cache__uuid_dir(paths.DEFAULT_CACHE_HASH_DIR, create_subfolder=False)
    collections.debugger("Creating 'hashsum' structure...", use_time=False)
    _add_to_cache__writer(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "hashsum"), os.path.join(paths.DEFAULT_CACHE_HASH_DIR, huid[:2], huid[2:]))
    _add_to_cache__writer(os.path.join(paths.DEFAULT_CACHE_HASH_DIR, huid[:2], huid[2:]), snapshot.get_hash_from_file(file))
    buid = _add_to_cache__uuid_dir(paths.DEFAULT_CACHE_COPY_DIR, create_subfolder=False)
    collections.debugger("Creating 'bitsfile' structure...", use_time=False)
    _add_to_cache__writer(os.path.join(paths.DEFAULT_CACHE_META_DIR, uid[:2], uid[2:], "bitsfile"), os.path.join(paths.DEFAULT_CACHE_COPY_DIR, buid[:2], buid[2:]))
    with open(os.path.join(paths.DEFAULT_CACHE_COPY_DIR, buid[:2], buid[2:]), "xb") as f:
        ret = snapshot.get_bytes_from_file(file, byte_arr)
        for x in range(len(ret)):
            f.write(ret[x])
        f.close()
        
def del_from_cache(file_uuid: str):
    try:
        path = paths.DEFAULT_CACHE_META_DIR
        first_dir = file_uuid[:2]
        second_dir = file_uuid[2:]
        hashsum_file = os.path.normpath(default.get_line_from_file(os.path.join(path, first_dir, second_dir, "hashsum")))
        bits_file = os.path.normpath(default.get_line_from_file(os.path.join(path, first_dir, second_dir, "bitsfile")))
        os.remove(hashsum_file)
        os.remove(bits_file)
        os.remove(os.path.join(path, first_dir, second_dir, "filename"))
        os.rmdir(os.path.join(path, first_dir, second_dir))
        return True
    except:
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
            for y in range(len(temp_files)):
                collections.debugger(f"Working on '{meta_objects[x] + temp_files[y]}'", use_time=False)
                name = " "
                hashsum = " "
                bitsfile = " "
                if_found = 0
                with open(os.path.join(metadir, meta_objects[x], temp_files[y], "filename")) as f:
                    name = f.readline().lstrip().rstrip()
                    collections.debugger(f"Found filename '{name}'", use_time=False)
                    if name == file:
                        collections.debugger(f"FOUND file '{file}'", use_time=False)
                        if_found = 1
                    f.close()
                if if_found:
                    #collections.debugger("Prepare to check hashsum, if bits will not examing...")
                    with open(os.path.join(metadir, meta_objects[x], temp_files[y], "hashsum")) as f:
                        hashsum = f.readline().rstrip().lstrip()
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
        collections.exceptor("Cannot do latest job, because raised: " + str(e), short=True, exception_do=1)
        return False, []
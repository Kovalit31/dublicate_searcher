#!/usr/bin/env python3.9
from copy import deepcopy
import os
import sys

from .plugins import collections, config
from .utils import cacher, paths, snapshot


def _check_consistent(_uuid: str, byte_arr: list):
    try:
        exists_in_cache, data_from_cache = cacher.get_cache_data_by_uuid(_uuid)
        if exists_in_cache:
            cached_hashsum, byte_file = data_from_cache
        else:
            collections.exceptor(f"No found file with this uuid {_uuid}!", short=True, exception_do=2)
        need_to_check_hash = 0
        file_path = cacher.get_cached_path_by_uuid(_uuid)
        hash_real = " "
        bytes_cached = []
        bytes_real = snapshot.get_bytes_from_file(file_path, byte_arr)
        collections.debugger(f"Getting bytes from file: {byte_file}", use_time=False, short=True)
        with open(byte_file, "rb") as opened_byte_file:
            opened_byte_file_length = len(bytearray(opened_byte_file.read()))
            for x in range(len(opened_byte_file_length)):
                opened_byte_file.seek(x + 1)
                bytes_cached.append(opened_byte_file.read(1))
        if len(bytes_cached) == len(bytes_real):
            for x in range(len(bytes_real)):
                if not bytes_real[x] == bytes_cached[x]:
                    need_to_check_hash = 1
                    break
            else:
                return True
        else:
            need_to_check_hash
        if need_to_check_hash:
            collections.debugger(f"Checking hash, because bits is broken: {file_path}", use_time=False, short=True)
            hash_real = snapshot.get_hash_from_file(file_path)
            if cached_hashsum.strip().lower() == hash_real.strip().lower():
                return True
            else:
                return False
    except:
        return False

def main(_path: str):
    files_will_cached = []
    uuids_of_cached_files = []
    byte_arr = [73, 76, 485, 35, 456]
    
    for root, dirs, files in os.walk(_path):
        collections.debugger("In main: ", [root, files], use_time=False)
        for x in range(len(files)):
            files_will_cached.append(os.path.join(root, files[x]))
    
    total_files_will_cached = len(files_will_cached)
    total_files_is_cached = 0

    collections.info("It was caching and, if need, fixing cache...", short=True)
    collections.debugger("Working on cache!", use_time=False, short=True)

    for file_will_cached_pos in range(len(files_will_cached)):
        try:
            collections.info(f"Processed {total_files_is_cached} from {total_files_will_cached}...", short=True)
            collections.debugger("Finding file: ", [files_will_cached[file_will_cached_pos]], use_time=False, short=True)
            exist_in_cache, cached_uuid = cacher.find_in_cache(files_will_cached[file_will_cached_pos])
            cache_is_consistent = False
            if exist_in_cache:
                collections.debugger("It exist", use_time=False, short=True)
                if _check_consistent(cached_uuid, byte_arr):
                    collections.debugger("It good", use_time=False, short=True)
                    cache_is_consistent = True
                else:
                    collections.debugger("It bad", use_time=False, short=True)
                    cache_is_consistent = False
            else:
                collections.debugger("It not exist", use_time=False, short=True)
                cache_is_consistent = False
            if not cache_is_consistent:
                collections.debugger("Deleting it!", use_time=False, short=True)
                cacher.del_from_cache(cached_uuid)
                collections.debugger(f"Adding it with args: {files_will_cached[file_will_cached_pos]}, {byte_arr}", use_time=False, short=True) 
                _uuid = cacher.add_to_cache(files_will_cached[file_will_cached_pos], byte_arr)
            uuids_of_cached_files.append(cached_uuid)
            total_files_is_cached += 1
        except Exception as e:
            collections.exceptor(f"Cannot setup cache: {str(e)}", type=NotImplementedError, short=True, exception_do=2)
    
    found_dublicates = []
    copy_of_uuids = deepcopy(uuids_of_cached_files)
    total_uuids_count = len(copy_of_uuids)
    collections.info("It was finding dublicates...")
    while len(copy_of_uuids) > 0:
        collections.info(f"Processed {total_uuids_count - len(copy_of_uuids)} from {total_uuids_count}...", short=True)
        selected_uuid = copy_of_uuids[0]
        collections.debugger(f"Selected uuid: {selected_uuid}", use_time=False, short=True)
        other_uuids = deepcopy(copy_of_uuids[0:])
        exist_sel_uuid_in_cache, data_from_sel_cache = cacher.get_cached_data_by_uuid(selected_uuid)
        sel_cached_file_hashsum = data_from_sel_cache[0]
        collections.debugger("It's data: ", [exist_sel_uuid_in_cache, data_from_sel_cache, sel_cached_file_hashsum])
        dublicates_for_selected_uuid = []
        collections.debugger("Arrays initialized: ", [copy_of_uuids, other_uuids])
        for other_uuid in range(len(other_uuids)):
            exist_other_uuid_in_cache, other_uuid_data_from_cache = cacher.get_cached_data_by_uuid(other_uuid)
            other_cached_file_hashsum = other_uuid_data_from_cache[0]
            collections.debugger("Getting other uuid data: ", [exist_other_uuid_in_cache, other_uuid_data_from_cache, other_cached_file_hashsum])
            if sel_cached_file_hashsum == other_cached_file_hashsum:
                collections.debugger(f"Is dublicate with uuid: {other_uuids[other_uuid]}\nFilename: {cacher.get_cached_path_by_uuid(other_uuids[other_uuid])}", use_time=False, short=True)
                dublicates_for_selected_uuid.append(other_uuids[other_uuid])
        found_dublicates.append(deepcopy(dublicates_for_selected_uuid))
        for dublicate_uuid in range(len(dublicates_for_selected_uuid)):
            uuid_index = copy_of_uuids.index(dublicates_for_selected_uuid[dublicate_uuid])
            collections.debugger(f"Deleting uuid from filter: {dublicates_for_selected_uuid[dublicate_uuid]}", use_time=False, short=True)
            copy_of_uuids.pop(uuid_index)
    array_humaned = []
    for dublicates in range(len(found_dublicates)):
        array_humaned.append([])
        for dublicate in range(len(found_dublicates[dublicates])):
            array_humaned[x].append(cacher.get_cached_path_by_uuid(found_dublicates[dublicates][dublicate]))
    for dublicates_arr_humaned_pos in range(len(array_humaned)):
        collections.info(f"Dublicates for file {array_humaned[dublicates_arr_humaned_pos][0]}: {array_humaned[dublicates_arr_humaned_pos][1:]}", short=True)
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        a = input("Path to work:")
    else:
        a = sys.argv[1]
    _path = os.path.realpath(a)
    main(_path)

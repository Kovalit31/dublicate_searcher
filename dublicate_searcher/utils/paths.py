import os
import pathlib

DEFAULT_DIR = os.path.join(pathlib.Path.home(), ".dublicate_pysearcher")
DEFAULT_CACHE_DIR = os.path.join(DEFAULT_DIR, "cache")
DEFAULT_CACHE_COPY_DIR = os.path.join(DEFAULT_CACHE_DIR, "bits")
DEFAULT_CACHE_META_DIR = os.path.join(DEFAULT_CACHE_DIR, "meta")

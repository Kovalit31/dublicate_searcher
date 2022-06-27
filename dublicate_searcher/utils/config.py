import pathlib
import os
from . import default

def get_config_path():
    return os.path.join(pathlib.Path.home(), ".dublicate_pyfinder", "config")

def get_default(config_string):
    pass

def comfig_parse(config_string):
    config_path = get_config_path()
    tokens = {}
    try:
        with open(config_path) as f:
            for line in f.readlines():
                line.rstrip().lstrip()
                _ = line.split("=")
                _[0].lstrip().rstrip()
                _[1].lstrip().rstrip()
                tokens[_[0]] = _[1]
        
    except:
        try:
            return default.config[config_string]
        except:
            return None

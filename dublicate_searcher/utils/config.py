import pathlib
import os
from . import default

def get_config_path():
    return os.path.join(pathlib.Path.home(), ".dublicate_pyfinder", "config")

def create_conf():
    try:
        os.makedirs(os.path.join(pathlib.Path.home(), ".dublicate_pyfinder"))
    except:
        pass
    try:
        with open(get_config_path(), "x") as f:
            f.write()
            f.close()
    except:
        pass

def config_parse(config_string):
    config_path = get_config_path()
    tokens = {}
    try:
        with open(config_path) as f:
            for line in f.readlines():
                if not line.lstrip().startswith("#"):
                    _token = line.lower().split("=")
                    if len(_token) > 1:
                        if len(_token) < 3:
                            tokens[_token[0].lstrip().rstrip()] = _token[1].lstrip().rstrip()
                        else:
                            pass
                    else:
                        pass
        for token in tokens:
            if token == config_string:
                return tokens[token]
    except:
        try:
            create_conf()
        except:
            pass
        try:
            return default.config[config_string]
        except:
            return None

if __name__ == "__main__":
    print(config_parse("cpu_count"))

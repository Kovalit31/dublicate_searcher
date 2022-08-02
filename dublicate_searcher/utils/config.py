import os
import sys
import importlib
import importlib.util

def importer(module_path: str, name: str, package=__package__):
    '''
    Import module from path with importlib and returns:
    [1, module], if Sucessfull
    [0] if Fail
    '''
    try:
        spec = importlib.util.spec_from_file_location(name ,module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return [1, module]
    except Exception as e:
        print(e)
        return [0]

def understood_config(path_config: str):
    '''
    Getting to understand config with first line
    Example, if config starting with "###ini###"
    it tells, this is "ini" config
    '''
    try:
        with open() as f:
            pass
    except:
        pass

def get_default(default, config_string):
    pass

def _create_default_config_ini(default, collection=None, legacy=1):
    '''
    Creates default config with ini markup
    '''
    try:
        os.makedirs(default.DEFAULT_CONFIG_DIR)
    except:
        pass
    try:
        text = "###ini###\n# Config\n"
        # Except, if config lenght is less than 2
        if len(default.config) < 2:
            if legacy:
                raise Exception("Default config is writed incorrectly, skipping")
            else:
                collection.exceptor("Default config is writed incorrect!")
        
        # Parsing arrays
        sections_names_arr = default.config[0]
        sections_vars_arr = default.config[1]
        sections_helps_arr = []
        if len(default.config) > 2:
            sections_helps_arr = default.config[2]
        else:
            sections_helps_arr = []
        
        # Lengths of arrays
        sections_names_arr_len = len(sections_names_arr)
        sections_vars_arr_len = len(sections_vars_arr)
        sections_helps_arr_len = len(sections_helps_arr)
        
        # Enumerate sections ( Trasmiss fizical and logical sections to one variable )
        sections_names_enum = 0
        if sections_names_arr_len >= sections_vars_arr_len:
            sections_names_enum = sections_vars_arr_len
        else:
            sections_names_enum = sections_names_arr_len
            
        # Enumerate helps
        sections_helps_enum = 0
        if sections_helps_arr_len >= sections_names_arr_len:
            sections_helps_enum = sections_names_arr_len
        else:
            sections_helps_enum = sections_helps_arr_len
        
        # Section mapping
        for x in range(sections_names_enum):
            # Define variabes for current section
            section_name = sections_names_arr[x]
            section_vars_arr = sections_vars_arr[x]
            section_help = ""
            if sections_helps_enum >= x + 1:
                section_help = sections_helps_arr[x]
            else:
                section_help = False
            
            # Adding initial lines for section (ini)
            if not legacy:
                collection.debugger("Contactation at x", [x])
            if type(section_name) == str:
                text += "[" + section_name.upper() + "]\n"
            elif not type(section_name) == int or not type(section_name) == bool:
                text += "[" + "/".join(section_name).upper() + "]\n"
            else:
                if not legacy:
                    collection.exceptor("Config writed incorrectly!")
                else:
                    raise Exception("Config writed incorrectly!")
            if not legacy:
                collection.debugger("Contactation at x", [x, section_help])
            if section_help:
                text += "# " + section_help + "\n"
            
            # Parsing variable arrays
            section_vars_names = section_vars_arr[0]
            section_vars_values = section_vars_arr[1]
            section_vars_helps = []
            if len(section_vars_arr) > 2:
                section_vars_helps = section_vars_arr[2]
            else:
                section_vars_helps = []
            
            # Adding array lengths for current section
            section_vars_names_len = len(section_vars_names)
            section_vars_values_len = len(section_vars_values)
            section_vars_helps_len = len(section_vars_helps)
            
            # Enumerate vars per x section
            section_vars_names_enum = 0
            if section_vars_names_len >= section_vars_values_len: # If names is more than variables
                section_vars_names_enum = 1
            else: 
                section_vars_names_enum = 0
            
            # Enumerate helps per x var
            
            section_vars_helps_enum = 0
            if section_vars_names_len >= section_vars_helps_len:
                section_vars_helps_enum = section_vars_helps_len
            else:
                section_vars_helps_enum = section_vars_names_len
            
            for y in range(len(section_vars_arr[section_vars_names_enum])):
                if not legacy:
                    collection.debugger("Contactation at y", [x, y])
                if not type(section_vars_arr[1][y]) == str:
                    text += str(section_vars_arr[0][y]).upper() + " = " + str(section_vars_arr[1][y]) + "\n"
                else:
                    text += str(section_vars_arr[0][y]).upper() + " = \"" + section_vars_arr[1][y] + "\"\n"
        try:
            with open(os.path.join(default.DEFAULT_CONFIG_DIR, default.DEFAULT_CONFIG_NAME), "x") as f:
                f.write(text)
                f.close()
        except:
            if not legacy:
                collection.debugger("Config already exists")
        return True
    except Exception as e:
        print(e)
        return False

def create_default_config(default_config_module_path=os.path.join(os.path.dirname(__file__), "config", "default.py")):
    '''
    Main "head", what is working with _create_default_config_<type>
    '''
    legacy = 0
    arr = importer(os.path.join(os.path.dirname(__file__), "collections.py"), 'collection')
    if arr[0]:
        collection = arr[1]
    else:
        legacy = 1
    del(arr)
    arr = importer(default_config_module_path, "default")
    if arr[0]:
        default = arr[1]
    else:
        try:
            os.makedirs(os.path.join(os.path.dirname(__file__), "config"))
        except:
            if not legacy:
                collection.debugger("Cannot create dir '{0}': File exists".format(os.path.join(os.path.dirname(__file__), "config")))
        try:
            with open(default_config_module_path, "x") as f:
                f.close()
        except:
            if not legacy:
                collection.exceptor()
            else:
                raise Exception()
        if not legacy:
            collection.exceptor(f"Cannot load default configuration: setup new configuration in '{default_config_module_path}' at yourself", type="ImportError", thread="config/create_default_config")
        else:
            raise ImportError(f"Cannot load default configuration: setup new configuration in '{default_config_module_path}' at yourself")
    del(arr)
    answer = None
    if default.DEFAULT_CONFIG_TYPE == "ini":
        answer = _create_default_config_ini(default, collection, legacy)
    if answer == False:
        if os.path.exists(os.path.join(default.DEFAULT_CONFIG_DIR, default.DEFAULT_CONFIG_NAME)) and not os.path.isdir(os.path.join(default.DEFAULT_CONFIG_DIR, default.DEFAULT_CONFIG_NAME)):
            if not legacy:
                collection.debugger("Cannot create config: it exists", thread="config/create_default_config")
        else:
            if not legacy:
                collection.exceptor("Error with creating config!", type="ConfigError", thread="config/create_default_config")
            else:
                raise Exception("Error with creating config!")

def _read_default_config_ini(section: str, setting: str, default, collection=None, legacy=1):
    pass

def read_default_config(config_string: str, default_config_module_path=os.path.join(os.path.dirname(__file__), "config", "default.py")):
    '''
    Main "head", what works with _read_default_config_<type>
    '''
    legacy = 0
    arr = importer(os.path.join(os.path.dirname(__file__), "collections.py"), "collection")
    if arr[0]:
        collection = arr[1]
    else:
        legacy = 1
    del(arr)
    arr = importer(default_config_module_path, "default")
    if arr[0]:
        default = arr[1]
    else:
        try:
            os.makedirs(os.path.join(os.path.dirname(__file__), "config"))
        except:
            if not legacy:
                collection.debugger("Cannot create dir '{0}': File exists".format(os.path.join(os.path.dirname(__file__), "config")))
        try:
            with open(default_config_module_path, "x") as f:
                f.close()
        except:
            if not legacy:
                collection.exceptor()
            else:
                raise Exception()
        if not legacy:
            collection.exceptor(f"Cannot load default configuration: setup new configuration in '{default_config_module_path}' at yourself", type="ImportError", thread="config/create_default_config")
        else:
            raise ImportError(f"Cannot load default configuration: setup new configuration in '{default_config_module_path}' at yourself")
    del(arr)
    answer = None
    if default.DEFAULT_CONFIG_TYPE == "ini":
        section, setting, *other = config_string.lstrip().rstrip().split(".")
        answer = _read_default_config_ini(section, setting, default, collection=collection, legacy=legacy)
    if answer == None:
        if not legacy:
            collection.debugger(f"No config string found: {config_string}")

# def update_default_config():
#     pass
# Test
if __name__ == "__main__":
    create_default_config()

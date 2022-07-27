import os
from . import paths

config = [
    [ # Names of sections
        "cpu", 
        "hash"
    ],
    [ # Settings for each section
        [ # CPU section
            ["core_count", "threads_per_core", "use_threads"], # Names
            [2,2,True], # Variables
            [] # Helps
        ], 
        [ # HASH section
            ["hash_len", "hash_type"],
            [1, "sha"]
        ]
    ],
    [ # Helps for each sections
        "This section provides faster hash computing.",
        "This section provides hash type and, if possible, hash lenght."
    ]
]


def parse():
    global config
    tokens = {}
    cfg_readed = []
    try:
        with open(paths.DEFAULT_CONFIG) as f:
            cfg_readed = f.readlines()
            f.close()
    except:
        try:
            os.makedirs(paths.DEFAULT_DIR)
        except:
            pass
        try:
            text = "# Config for PyDublicateSearcher\n"
            # Except, if config lenght is less than 2
            if len(config) < 2:
                raise Exception("Default config is writed incorrectly, skipping")
            
            # Lengths of arrays
            sections_arr_len = len(config[0])
            var_sections_arr_len = len(config[1])
            if len(config) > 2:
                section_help_arr_len = len(config[2])
            else:
                section_help_arr_len = 0
            
            # Enumerate sections ( Trasmiss fizical and logical sections to one variable )
            section_enum = 0
            if sections_arr_len >= var_sections_arr_len:
                section_enum = var_sections_arr_len
            else:
                section_enum = sections_arr_len
            
            # Enumerate helps
            helps_enum = 0
            if section_help_arr_len >= sections_arr_len:
                helps_enum = sections_arr_len
            else:
                helps_enum = section_help_arr_len
            
            # Section mapping
            for x in range(section_enum):
                # Define variabes for current section
                section_name = config[0][x]
                section_var_arr = config[1][x]
                if helps_enum >= x + 1 and len(config) > 2:
                    section_help = config[2][x]
                else:
                    section_help = False
                
                # Adding initial lines for section
                text += "[" + section_name.upper() + "]\n"
                if section_help:
                    text += "# " + section_help + "\n"
                
                # Adding array lengths for current section
                logical_section_settings_len = len(section_var_arr[0])
                fizical_section_settings_len = len(section_var_arr[1])
                ## if no help array, skipping  
                if len(section_var_arr) > 2:
                    section_settings_helps_len = len(section_var_arr[2])
                else:
                    section_settings_helps_len = 0
                
                # Enumerate settings per x section
                section_settings_enum = 0
                if logical_section_settings_len >= fizical_section_settings_len: # If names is more than variables
                    section_settings_enum = fizical_section_settings_len
                else: 
                    section_settings_enum = logical_section_settings_len
                
                for y in range(len(config[1][x][section_settings_enum])):
                    if not type(config[1][x][1][y]) == str:
                        text += str(config[1][x][0][y]).upper() + " = " + str(config[1][x][1][y]) + "\n"
                    else:
                        text += str(config[1][x][0][y]).upper() + " = \"" + config[1][x][1][y] + "\"\n"
            with open(paths.DEFAULT_CONFIG, "x") as f:
                f.write(text)
                f.close()
        except Exception as e:
            print(e)
    if len(cfg_readed) > 0:
        pass

if __name__ == "__main__":
    parse()

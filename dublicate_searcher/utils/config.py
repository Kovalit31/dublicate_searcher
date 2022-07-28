# ini parser
import os
from . import default
from .default import config


def create_default_config():
    global config
    try:
        os.makedirs(default.DEFAULT_CONFIG_DIR)
    except:
        pass
    try:
        text = "# Config\n"
        # Except, if config lenght is less than 2
        if len(config) < 2:
            raise Exception("Default config is writed incorrectly, skipping")
        
        # Parsing arrays
        sections_names_arr = config[0]
        sections_vars_arr = config[1]
        sections_helps_arr = [config[2] if len(config) > 2 else []]
        
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
            section_name = config[0][x]
            section_vars_arr = config[1][x]
            section_help = ""
            if sections_helps_enum >= x + 1 and len(config) > 2:
                section_help = config[2][x]
            else:
                section_help = False
            
            # Adding initial lines for section (ini)
            text += "[" + section_name.upper() + "]\n"
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
                if not type(config[1][x][1][y]) == str:
                    text += str(config[1][x][0][y]).upper() + " = " + str(config[1][x][1][y]) + "\n"
                else:
                    text += str(config[1][x][0][y]).upper() + " = \"" + config[1][x][1][y] + "\"\n"
        with open(os.path.join(default.DEFAULT_CONFIG_DIR, default.DEFAULT_CONFIG_NAME), "x") as f:
            f.write(text)
            f.close()
        return 0
    except Exception as e:
        print(e)
        return 1
# Test
if __name__ == "__main__":
    create_default_config()

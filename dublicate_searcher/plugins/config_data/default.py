import os
import pathlib

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

DEFAULT_CONFIG_DIR = os.path.join(pathlib.Path.home(), ".dublicate_pysearcher")
DEFAULT_CONFIG_NAME = "config.ini"
DEFAULT_CONFIG_TYPE = "ini"

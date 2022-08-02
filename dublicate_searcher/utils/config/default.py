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


DEFAULT_DIR = os.path.join(pathlib.Path.home(), ".dublicate_pysearcher")
DEFAULT_CONFIG_DIR = DEFAULT_DIR
DEFAULT_CONFIG_NAME = "config.ini"
DEFAULT_CACHE_DIR = os.path.join(DEFAULT_DIR, "cache")
DEFAULT_CACHE_COPY_DIR = os.path.join(DEFAULT_CACHE_DIR, "bits")
DEFAULT_CACHE_HASH_DIR = os.path.join(DEFAULT_CACHE_DIR, "hash")
DEFAULT_CACHE_META_DIR = os.path.join(DEFAULT_CACHE_DIR, "meta")
DEFAULT_CONFIG_TYPE = "ini"
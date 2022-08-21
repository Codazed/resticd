import os
import threading
from classes.daemon import daemon
from classes.config import config
from utils.config_parser import parse_config

parse_config('config.yml', config)

# Set up any directories
if not os.path.isdir(config.globals.restic_cache_dir):
    os.mkdir(config.globals.restic_cache_dir)

if not os.path.isdir(config.globals.restic_tmp_dir):
    os.mkdir(config.globals.restic_tmp_dir)

daemon_thread = threading.Thread(target=daemon().start(), daemon=True)

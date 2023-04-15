# routines/utils/setup_log.py
import logging
import os
from configparser import ConfigParser

## PARSING CONFIG FILE ##
config = ConfigParser()
config.read('config/config_default.ini')
LogLevel = config.get('GeneralSettings', 'LogLevel')
logging_level = getattr(logging, LogLevel.upper(), logging.INFO)
logging.getLogger().setLevel(logging_level)

def setup_logging(log_directory="logs", log_file_name="bot.log"):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, log_file_name)

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file_path, encoding="utf-8")
        ],
        datefmt="%d/%m/%Y %H:%M:%S --"
    )
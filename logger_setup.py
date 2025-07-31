# logger_setup.py
# Set up logging configuration for the whole app

import logging
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,               # Log file path
    level=logging.INFO,             # Log level (INFO and above)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',   # Timestamp format in logs
)

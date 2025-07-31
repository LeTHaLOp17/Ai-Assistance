# memory.py
# Functions to load and save persistent memory to JSON file

import json
import os
from config import MEMORY_FILE

def load_memory():
    """
    Load memory dictionary from JSON file.
    Return empty dict if file does not exist or is corrupted.
    """
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_memory(memory):
    """
    Save memory dictionary to JSON file.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

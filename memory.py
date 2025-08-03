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
        
def load_prefs():
    if os.path.exists("preferences.json"):
        with open("preferences.json", "r") as f:
            return json.load(f)
    return {}

def save_prefs(prefs):
    with open("preferences.json", "w") as f:
        json.dump(prefs, f, indent=4)


# config.py
# Load environment variables and define config constants

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file contents into environment variables

# API keys loaded from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# File paths used by the application
MEMORY_FILE = "memory.json"
LOG_FILE = "ai_assistant.log"

# Check if Gemini API key is present
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables (.env)")

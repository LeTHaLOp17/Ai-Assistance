import os
from dotenv import load_dotenv
import pyttsx3
import logging
import json

# Load environment variables from .env file (like API keys)
load_dotenv()

# ------------------- GOOGLE GEMINI SETUP -------------------
# You need to install google-genai package: pip install google-genai
import google.generativeai as genai

# Get your Google Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables (.env)")

# Set the API key so we can use the Google Gemini service
genai.configure(api_key=GEMINI_API_KEY)

# Choose which Gemini model you want to use
gemini_model = genai.GenerativeModel("gemini-2.5-flash")
# You can also use "gemini-1.5-flash" or "gemini-1.5-pro" if you want

# ----------------- OPENAI SETUP (COMMENTED OUT) -----------------
"""
import openai

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables (.env)")

# Initialize OpenAI client (not used now)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
"""

# ----------------- Setup text-to-speech -----------------
# Initialize pyttsx3 text-to-speech engine to read AI responses aloud
tts_engine = pyttsx3.init()

# ----------------- Setup logging -----------------
# Configure logging to save info and errors into a log file with timestamps
logging.basicConfig(
    filename='ai_assistant.log',  # The log file name
    level=logging.INFO,           # Log info-level messages and above
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',                        # Date/time format in logs
)

# ----------------- Memory file configuration -----------------
MEMORY_FILE = "memory.json"

# Function to load memory from a JSON file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)  # Load and return the saved memory dictionary
        except json.JSONDecodeError:
            return {}  # If file is corrupted, return empty memory
    return {}  # If file doesn't exist, return empty memory

# Function to save memory dictionary to a JSON file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)  # Save memory with indentation for readability

# Function to print, speak, and log the AI response
def speak(text: str):
    print("AI:", text)             # Print AI response to console
    tts_engine.say(text)           # Have TTS engine say the text aloud
    tts_engine.runAndWait()        # Wait until speaking is finished
    logging.info(f"AI response spoken: {text}")  # Log the AI response

# Main program loop that runs the assistant
def main():
    # Load saved memory before starting
    memory = load_memory()

    print("Welcome to your AI assistant (Google Gemini). Type 'exit' or 'quit' to stop.")
    logging.info("Session started.")  # Log that session has started

    while True:
        user_input = input("You: ").strip()   # Get user input from console
        logging.info(f"User input: {user_input}")  # Log the user input
        user_input_lower = user_input.lower()      # For easier comparison

        # If user wants to quit, exit the program
        if user_input_lower in ["exit", "quit"]:
            print("Goodbye! Have a great day!")
            logging.info("User exited the assistant.")
            break

        # Check if user wants to teach the assistant something new
        if user_input_lower.startswith("remember ") and " is " in user_input_lower:
            try:
                # Extract the key and value from "remember X is Y"
                rest = user_input[8:]  # Remove "remember " from the start
                key, value = rest.split(" is ", 1)  # Split into key and value
                key = key.strip().lower()     # Clean up key (lowercase for consistency)
                value = value.strip()         # Clean up value

                memory[key] = value            # Save into memory dictionary
                save_memory(memory)            # Save dictionary to file

                speak(f"Okay, I will remember {key} is {value}.")  # Confirm to user
                continue  # Skip AI API call since this is handled here
            except Exception:
                speak("Sorry, please say it like 'remember X is Y'.")
                continue

        # Check if user asks for something from memory
        if user_input_lower.startswith("what is "):
            key = user_input_lower[8:].strip()      # Extract key from question
            if key in memory:
                speak(f"{key} is {memory[key]}")    # Respond with stored value
            else:
                # If unknown, prompt user to teach assistant
                speak(f"I don't know what {key} is yet. You can teach me by saying 'remember {key} is ...'")
            continue  # Skip AI API call since handled here

        # Otherwise, query the AI model for answer

        # Create system prompt to guide AI response
        system_prompt = "You are a helpful, friendly AI assistant."
        # Format prompt with system and user message for Gemini input
        prompt_text = f"{system_prompt}\nUser: {user_input}\nAssistant:"

        try:
            # Call Google Gemini API to generate AI response
            response = gemini_model.generate_content(
                prompt_text,
                generation_config={
                    "max_output_tokens": 2048,  # Maximum length of response tokens
                    "temperature": 0.9          # Creativity of the response (0-1)
                }
            )
            ai_reply = response.text.strip()   # Get the text response
            logging.info(f"Google Gemini response: {ai_reply}")  # Log response
            speak(ai_reply)  # Speak and print the AI response

            # ----- OpenAI equivalent code (kept for future use, commented out) -----
            """
            messages = [
                {"role": "system", "content": "You are a helpful, friendly AI assistant."},
                {"role": "user", "content": user_input},
            ]
            openai_response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or "gpt-4"
                messages=messages,
            )
            ai_reply = openai_response.choices[0].message.content.strip()
            logging.info(f"OpenAI response: {ai_reply}")
            speak(ai_reply)
            """
        except Exception as e:
            error_msg = f"Error communicating with AI API: {e}"
            print(error_msg)           # Show error to user
            logging.error(error_msg)   # Log error for debugging

if __name__ == "__main__":
    main()
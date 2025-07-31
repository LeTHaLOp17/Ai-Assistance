import os
from dotenv import load_dotenv
import openai
import pyttsx3
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Initialize OpenAI client with key from .env
client = openai.OpenAI(api_key=api_key)

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Configure logging to file with timestamps
logging.basicConfig(
    filename='ai_assistant.log',
    level=logging.INFO,  # Change to DEBUG for more verbose logs if needed
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def speak(text):
    """Prints and speaks the AI response, and logs it."""
    print("AI:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()
    logging.info(f"AI response spoken: {text}")

def main():
    print("Welcome to your AI assistant. Type 'exit' or 'quit' to stop.")
    logging.info("Session started.")

    while True:
        user_input = input("You: ").strip()
        logging.info(f"User input: {user_input}")

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! Have a great day!")
            logging.info("User exited the assistant.")
            break

        # Prepare messages for OpenAI chat completion
        messages = [
            {"role": "system", "content": "You are a helpful, friendly AI assistant."},
            {"role": "user", "content": user_input},
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",   # or "gpt-4" if you have access
                messages=messages
            )
            ai_reply = response.choices[0].message.content.strip()
            logging.info(f"AI response received: {ai_reply}")
            speak(ai_reply)

        except Exception as e:
            error_msg = f"Error communicating with OpenAI API: {e}"
            print(error_msg)
            logging.error(error_msg)

if __name__ == "__main__":
    main()
# This code is the main entry point for the AI assistant application.
# It initializes the OpenAI client, sets up text-to-speech, and handles user input
# to provide responses from the AI model. It also logs interactions for debugging and analysis.
# Ensure that the OpenAI API key is set in the environment variables.
# This file is part of the AI Assistant project.
# Do not modify the API key directly in this file; use the .env file for configuration
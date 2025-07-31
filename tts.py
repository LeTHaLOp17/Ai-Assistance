# tts.py
# Text-to-speech utilities using pyttsx3

import pyttsx3
import logging

# Initialize TTS engine once for performance
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Set slower speech rate (optional)

def speak(text):
    """
    Print and speak the text aloud.
    Also logs the message for record.
    """
    print("AI:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()
    logging.info(f"AI response spoken: {text}")

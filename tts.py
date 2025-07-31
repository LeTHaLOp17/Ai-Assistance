import pyttsx3
import logging
import time

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Moderate slow speed
tts_engine.setProperty('volume', 1.0)  # Full volume

def speak(text):
    """
    Print and speak the text aloud.
    Also logs the message for record.
    """
    try:
        print("AI:", text)
        tts_engine.say(text)
        tts_engine.runAndWait()
        time.sleep(0.2)  # Small pause to ensure speech finishes
        logging.info(f"AI response spoken: {text}")
    except Exception as e:
        logging.error(f"TTS error: {e}")
        print(f"TTS Error: {e}")

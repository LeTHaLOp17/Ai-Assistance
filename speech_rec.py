import speech_recognition as sr

def streaming_recognize_speech(language='en-IN', device_index=0):
    """
    Simple speech-to-text via Google Web Speech (no Cloud/billing/key needed).
    `language`: e.g. 'en-IN' for Indian English, 'hi-IN' for Hindi.
    `device_index`: mic index (MacBook Air mic is 0 for you).
    """
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        print("Please say something!")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=7, phrase_time_limit=7)
    try:
        text = r.recognize_google(audio, language=language)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

if __name__ == "__main__":
    print("You said:", streaming_recognize_speech(device_index=0))

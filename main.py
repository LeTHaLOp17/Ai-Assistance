import logging
from memory import load_memory, save_memory, load_prefs, save_prefs
from conversation_log import load_history, append_history
from ai_client import get_ai_response, smart_speak
from tts import speak
import webbrowser
from speech_rec import streaming_recognize_speech


def get_user_command():
    print("Listening for your command...")
    try:
        command = streaming_recognize_speech()
        if command:
            print(f"You said: {command}")
            return command
        else:
            speak("Sorry, I didn't catch that. Bol na, yaar!")
            return None
    except Exception as e:
        print(f"Command listening error: {e}")
        speak("Sorry, kuch gadbad ho gayi. Dobara bolo!")
        return None

def main():
    logging.info("Assistant started!")
    memory = load_memory()
    print("Assistant is listening... (say 'exit' or 'quit' to stop)")
    while True:
        user_input = get_user_command()
        if not user_input: continue
        user_input_lower = user_input.lower()

        if user_input_lower in ["exit", "quit"]:
            speak("Goodbye, boss! Khayal rakhna!")
            break

        # Skills
        if user_input_lower.startswith("weather in ") or user_input_lower.startswith("what's the weather in "):
            from skills.weather import get_weather
            city = user_input_lower.replace("weather in ", "").replace("what's the weather in ", "").strip()
            report = get_weather(city or "Delhi")
            speak(report)
            continue

        if user_input_lower in ["daily briefing", "give me daily briefing", "morning briefing"]:
            from skills.daily_briefing import get_daily_briefing
            get_daily_briefing()
            continue

        if user_input_lower.startswith("my favorite"):
            parts = user_input_lower.split(" is ")
            if len(parts) == 2:
                key = parts[0].replace("my favorite", "").strip()
                value = parts[1].strip()
                prefs = load_prefs()
                prefs[key] = value
                save_prefs(prefs)
                speak(f"Arrey, mast! Apka favourite {key} hai {value}. Yaad rakhoonga.")
            continue

        if "open google" in user_input_lower:
            speak("Google khol raha hoon abhi.")
            webbrowser.open("https://google.com")
            continue

        if "open youtube" in user_input_lower:
            speak("YouTube aapke liye khol raha hoon!")
            webbrowser.open("https://youtube.com")
            continue

        if "remind me" in user_input_lower and " at " in user_input_lower:
            import re
            match = re.match(r".*remind me to (.+) at (.+)", user_input_lower)
            if match:
                message, time_str = match.groups()
                from skills.reminders import schedule_reminder
                schedule_reminder(message, time_str)
                speak(f"Reminder set kar diya, kuch aur boss?")
            continue

        if user_input_lower.startswith("remember ") and " is " in user_input_lower:
            try:
                logging.info(f"Processing remember command: {user_input}")
                rest = user_input[8:].split(" is ", 1)
                if len(rest) != 2:
                    raise ValueError("Invalid format.")
                key, value = rest[0].strip().lower(), rest[1].strip()
                memory[key] = value
                save_memory(memory)
                speak(f"Ho gaya! {key} ko {value} yaad rakh liya.")
            except Exception:
                speak("Galat format hai, 'remember X is Y' bolo.")
            continue

        if user_input_lower.startswith("what is "):
            key = user_input_lower[8:].strip()
            if key in memory:
                speak(f"Arrey, {key} hai {memory[key]}")
            else:
                speak(f"Mujhe abhi {key} nahi pata. Kahein to yaad kara doon?")
            continue

        # Default: AI conversation
        try:
            speak("Ek second, soch raha hoon, yaar...")
            ai_reply = get_ai_response(user_input)
            append_history({"user": user_input, "ai": ai_reply})
            smart_speak(ai_reply)
        except Exception as e:
            speak("Sorry, kuch error ho gaya! Thoda baad me fir try karein.")

if __name__ == "__main__":
    main()

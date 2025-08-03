# skills/daily_briefing.py
import datetime

from tts import speak

def get_weather(city="Your city"):
    # For demo, you can extend this with real API calls (OpenWeatherMap, etc.)
    return f"The weather in {city} today is sunny with a high of 28 degrees Celsius."

def get_events():
    # Placeholder: fetch calendar events or reminders here
    return ["You have a meeting at 10 AM.", "Doctor appointment at 3 PM."]

def get_news_headlines():
    # Placeholder: integrate a news API or static headlines for demo
    return [
        "Global markets show positive trends today.",
        "Scientists announce a breakthrough in renewable energy.",
    ]

def get_daily_briefing():
    today = datetime.date.today().strftime("%A, %B %d")
    speak(f"Good morning! Today is {today}.")

    weather = get_weather()
    speak(weather)

    events = get_events()
    if events:
        speak("Here are your scheduled events for today:")
        for event in events:
            speak(event)
    else:
        speak("You have no events scheduled today.")

    news = get_news_headlines()
    speak("Here are some news headlines to start your day:")
    for headline in news:
        speak(headline)

    speak("That is your daily briefing. Let me know if you want details on any topic.")

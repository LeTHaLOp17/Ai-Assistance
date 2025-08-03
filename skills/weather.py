# skills/weather.py
import requests
from config import OPENWEATHER_API_KEY

def get_weather(city="Mumbai"):
    if not OPENWEATHER_API_KEY:
        return "Weather service is not configured."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("cod") != 200:
            return f"Sorry, I couldn't get weather data for {city.title()}."
        desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        return f"{desc} in {city.title()} with a temperature of {temp}°C (feels like {feels}°C)."
    except Exception as e:
        return "I couldn't retrieve the weather right now."

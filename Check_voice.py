import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for index, voice in enumerate(voices):
    print(f"Voice {index}:")
    print(f" - ID: {voice.id}")
    print(f" - Name: {voice.name}")
    print(f" - Languages: {voice.languages}")
    print(f" - Gender: {voice.gender if hasattr(voice, 'gender') else 'N/A'}")
    print(f" - Age: {voice.age if hasattr(voice, 'age') else 'N/A'}")
    print('--------------------------')
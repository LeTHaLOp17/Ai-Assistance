# import speech_recognition as sr

# def test_mic():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Please say something:")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             print("You said:", text)
#         except sr.UnknownValueError:
#             print("Sorry, I could not understand audio")
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))

# if __name__ == "__main__":
#     test_mic()

# import pyaudio
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"Device {i}: {info['name']} {'(default)' if info['defaultSampleRate'] == 44100 else ''}")



import speech_recognition as sr

print(sr.Microphone.list_microphone_names())
r = sr.Recognizer()
with sr.Microphone(device_index=0) as source:
    print("Testing mic... Say something!")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source, timeout=8, phrase_time_limit=8)

print("Got audio, now trying to recognize...")
try:
    # Try adding timeout here as well:
    text = r.recognize_google(audio, language='en-IN', show_all=False)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
except Exception as e:
    print(f"Unknown error: {e}")


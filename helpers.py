import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches

# Initialize text to speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for different voices

# Get geolocation based on IP
g = geocoder.ip('me')

# Load dictionary data (for translate function)
data = json.load(open('data.json'))

def speak(audio) -> None:
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def screenshot() -> None:
    """Take a screenshot and save it to specified path."""
    img = pyautogui.screenshot()
    img.save(r'C:\Users\Admin\Pictures\Screenshots\screenshot.png')

def cpu() -> None:
    """Report CPU usage and battery percentage."""
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage + " percent")

    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(str(battery.percent) + " percent")

def joke() -> None:
    """Speak 5 jokes."""
    for i in range(5):
        speak(pyjokes.get_jokes()[i])

def takeCommand() -> str:
    """Listen and recognize speech, return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')
    except Exception as e:
        # print(e)
        print('Say that again please...')
        return 'None'
    return query

def weather():
    """Fetch weather info using World Weather Online API and speak it."""
    try:
        city = g.city or "your location"
        api_key = 'a9aee7d060da410ca8860747251410'
        api_url = f"https://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city}&format=json&num_of_days=1"

        response = requests.get(api_url)
        data_json = response.json()

        if 'data' in data_json and 'current_condition' in data_json['data']:
            current = data_json['data']['current_condition'][0]

            temp_c = current['temp_C']
            weather_desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed_kmph = current['windspeedKmph']

            speak(f"Current location is {city}")
            speak(f"Weather type is {weather_desc}")
            speak(f"Temperature is {temp_c} degrees Celsius")
            speak(f"Humidity is {humidity} percent")
            speak(f"Wind speed is {wind_speed_kmph} kilometers per hour")
        else:
            speak("Sorry, I couldn't get the weather information right now.")
    except Exception as e:
        print(f"Error getting weather: {e}")
        speak("Sorry, something went wrong while fetching the weather.")

def translate(word):
    """Translate a word using local data.json dictionary with fuzzy matching."""
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x + ' instead? Respond with Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")
    else:
        speak("Word doesn't exist. Please double check it.")

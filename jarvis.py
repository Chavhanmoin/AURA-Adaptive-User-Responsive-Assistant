import os
import sys
import datetime
import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser
import smtplib
import cv2
from sys import platform
from dotenv import load_dotenv
from youtube import youtube
from news import speak_news, getNewsUrl
from OCR import OCR
from diction import translate
from helpers import *

# Load .env file
load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


class Jarvis:
    def __init__(self) -> None:
        if platform == "linux" or platform == "linux2":
            self.chrome_path = '/usr/bin/google-chrome'
        elif platform == "darwin":
            self.chrome_path = 'open -a /Applications/Google\\ Chrome.app'
        elif platform == "win32":
            self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        else:
            print('Unsupported OS')
            sys.exit(1)
        
        try:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.chrome_path))
        except:
            pass  # fallback to default browser if chrome registration fails

    def wishMe(self) -> None:
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            speak("Good Morning SIR")
        elif 12 <= hour < 18:
            speak("Good Afternoon SIR")
        else:
            speak('Good Evening SIR')

        weather()
        speak('I am JARVIS. Please tell me how can I help you SIR?')

    def sendEmail(self, to, content) -> None:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to, content)
            server.close()
            speak("Email has been sent!")
        except Exception as e:
            print("Email error:", e)
            speak('Sorry sir, not able to send email at the moment')

    def execute_query(self, query):
        query = query.lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)

        elif 'youtube downloader' in query:
            exec(open('youtube_downloader.py').read())

        elif 'voice' in query:
            # Switch voices (female voice = voices[1], male = voices[0])
            if 'female' in query:
                engine.setProperty('voice', voices[1].id)
            else:
                engine.setProperty('voice', voices[0].id)
            speak("Hello Sir, I have switched my voice. How is it?")

        elif 'jarvis are you there' in query:
            speak("Yes Sir, at your service")

        elif 'jarvis who made you' in query:
            speak("Yes Sir, my master built me with AI")

        elif 'open youtube' in query:
            webbrowser.get('chrome').open_new_tab('https://youtube.com')

        elif 'open amazon' in query:
            webbrowser.get('chrome').open_new_tab('https://amazon.com')

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'screenshot' in query:
            speak("taking screenshot")
            screenshot()

        elif 'open google' in query:
            webbrowser.get('chrome').open_new_tab('https://google.com')

        elif 'open stackoverflow' in query:
            webbrowser.get('chrome').open_new_tab('https://stackoverflow.com')

        elif 'play music' in query:
            # Adjust path as per your music location
            os.startfile("D:\\RoiNa.mp3")

        elif 'search youtube' in query:
            speak('What do you want to search on Youtube?')
            youtube(takeCommand())

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')

        elif 'search' in query:
            speak('What do you want to search for?')
            search = takeCommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is what I found for ' + search)

        elif 'location' in query:
            speak('What is the location?')
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is the location ' + location)

        elif 'your master' in query:
            if platform in ["win32", "darwin"]:
                speak('Moin and team are my masters. They created me.')
            elif platform in ["linux", "linux2"]:
                speak('Moin and team are my masters. They are running me right now.')

        elif 'your name' in query:
            speak('My name is JARVIS')

        elif 'who made you' in query:
            speak('I was created by my AI master in 2021')

        elif 'stands for' in query:
            speak('J.A.R.V.I.S stands for JUST A RATHER VERY INTELLIGENT SYSTEM')

        elif 'open code' in query:
            if platform == "win32":
                try:
                    os.startfile("code")
                except:
                    speak("VS Code not found")
            elif platform in ["linux", "linux2", "darwin"]:
                os.system('code .')

        elif 'shutdown' in query:
            if platform == "win32":
                os.system('shutdown /p /f')
            elif platform in ["linux", "linux2", "darwin"]:
                os.system('poweroff')

        elif 'your friend' in query:
            speak('My friends are Google assistant, Alexa, and Siri')

        elif 'github' in query:
            webbrowser.get('chrome').open_new_tab('https://github.com/gauravsingh9356')

        elif 'remember that' in query:
            speak("What should I remember sir?")
            rememberMessage = takeCommand()
            speak("You told me to remember: " + rememberMessage)
            with open('data.txt', 'w') as remember:
                remember.write(rememberMessage)

        elif 'do you remember anything' in query:
            with open('data.txt', 'r') as remember:
                speak("You told me to remember that: " + remember.read())

        elif 'sleep' in query or 'exit' in query or 'quit' in query:
            speak("Goodbye Sir, shutting down JARVIS")
            sys.exit()

        elif 'dictionary' in query:
            speak('What do you want to search in your intelligent dictionary?')
            translate(takeCommand())

        elif 'news' in query:
            speak('Of course sir..')
            speak_news()
            speak('Do you want to read the full news?')
            test = takeCommand()
            if 'yes' in test:
                speak('Ok Sir, opening browser...')
                webbrowser.open(getNewsUrl())
                speak('You can now read the full news from this website.')
            else:
                speak('No problem sir.')

        elif 'email to gaurav' in query:
            try:
                speak('What should I say?')
                content = takeCommand()
                to = EMAIL  # sending email to your configured EMAIL
                self.sendEmail(to, content)
            except Exception:
                speak('Sorry sir, not able to send email at the moment')


def wakeUpJARVIS():
    bot_ = Jarvis()
    bot_.wishMe()
    try:
        while True:
            query = takeCommand().lower()
            bot_.execute_query(query)
    except KeyboardInterrupt:
        speak("Goodbye Sir, shutting down JARVIS")
        sys.exit(0)


if __name__ == '__main__':
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    recognizer.read('./Face-Recognition/trainer/trainer.yml')  # load trained model
    cascadePath = "./Face-Recognition/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)  # initializing haar cascade for object detection approach

    font = cv2.FONT_HERSHEY_SIMPLEX  # font type

    id = 2  # number of persons you want to Recognize

    names = ['', 'Moin']  # names, leave first empty because counter starts from 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()  # read the frames

        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id_, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])

            if accuracy < 100:
                speak("Optical Face Recognition Done. Welcome")
                cam.release()
                cv2.destroyAllWindows()
                wakeUpJARVIS()
            else:
                speak("Optical Face Recognition Failed")
                break

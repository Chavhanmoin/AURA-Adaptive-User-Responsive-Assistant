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
import openai
import os
from youtube import youtube
from news import speak_news, getNewsUrl
from OCR import OCR
from diction import translate
from helpers import *
from system_control import open_anything, close_anything, execute_system_command
import speech_recognition as sr
from web_automation import search_google, search_youtube, send_whatsapp_message, compose_gmail, close_web_automation
from intent_recognition import process_user_intent
from ai_intent_recognition import get_ai_intent

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
        # Always try AI intent first (with better fallback)
        try:
            ai_intent = get_ai_intent(query)
            print(f"AI Intent: {ai_intent}")
            if ai_intent['confidence'] > 0.5:
                return self.handle_ai_intent(ai_intent)
        except Exception as e:
            print(f"AI processing failed: {e}")
        
        # Fallback to rule-based intent
        intent_data = process_user_intent(query)
        if intent_data['intent'] and intent_data['confidence'] > 0.3:
            return self.handle_intent(intent_data)
        
        # Original processing as last resort
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
        
        elif 'open file' in query or 'open folder' in query:
            speak('What file or folder should I open?')
            path = takeCommand()
            result = open_anything(path)
            speak(result)

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

        elif 'youtube' in query and 'search' in query:
            search_term = query.replace('youtube', '').replace('search', '').replace('open', '').replace('and', '').strip()
            if search_term and len(search_term) > 1:
                result = search_youtube(search_term)
                print(result)
                speak(result)
            else:
                speak('What do you want to search on Youtube?')
                search_term = takeCommand()
                if search_term != 'None':
                    result = search_youtube(search_term)
                    print(result)
                    speak(result)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')

        elif 'search' in query and 'youtube' not in query:
            # Extract search term from query or ask for it
            search_term = query.replace('search', '').replace('for', '').strip()
            if not search_term or len(search_term) < 2:
                speak('What do you want to search for?')
                search_term = takeCommand()
            
            if search_term != 'None':
                result = search_google(search_term)
                print(result)
                speak(result)
            else:
                speak('No search term provided')

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

        elif 'open' in query and 'code' not in query:
            item = query.replace('open', '').replace('folder', '').strip()
            if 'download' in item:
                item = 'downloads'
            result = open_anything(item)
            print(result)
            speak(result)
        
        elif 'close' in query:
            item = query.replace('close', '').strip()
            result = close_anything(item)
            speak(result)
        
        elif 'run command' in query or 'execute' in query:
            speak('What command should I execute?')
            command = takeCommand()
            result = execute_system_command(command)
            speak('Command executed')
            print(result)

        elif 'open code' in query:
            result = open_anything('code')
            speak(result)

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
            close_web_automation()
            speak("Goodbye Sir, shutting down JARVIS")
            sys.exit()
    
    def handle_intent(self, intent_data):
        """Handle recognized intents"""
        intent = intent_data['intent']
        entities = intent_data['entities']
        
        if intent == 'open_app' and 'app' in entities:
            result = open_anything(entities['app'])
            speak(result)
            return
        
        elif intent == 'close_app' and 'app' in entities:
            result = close_anything(entities['app'])
            speak(result)
            return
        
        elif intent == 'search_google' and 'query' in entities:
            result = search_google(entities['query'])
            speak(result)
            return
        
        elif intent == 'search_youtube' and 'query' in entities:
            result = search_youtube(entities['query'])
            speak(result)
            return
        
        elif intent == 'time_query':
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
            return
        
        elif intent == 'system_info':
            cpu()
            return
        
        elif intent == 'joke':
            joke()
            return
        
        elif intent == 'weather_query':
            weather()
            return
        
        # If intent recognized but entities missing, ask for clarification
        if intent == 'open_app':
            speak('Which application should I open?')
        elif intent == 'search_google':
            speak('What should I search for?')
        elif intent == 'search_youtube':
            speak('What should I search on YouTube?')
    
    def handle_ai_intent(self, ai_intent):
        """Handle AI-recognized intents"""
        intent = ai_intent['intent']
        entities = ai_intent['entities']
        
        if intent == 'open_app':
            app = entities.get('app', entities.get('application', ''))
            if app:
                result = open_anything(app)
                speak(result)
            else:
                speak('Which application should I open?')
            return
        
        elif intent == 'close_app':
            app = entities.get('app', entities.get('application', ''))
            if app:
                result = close_anything(app)
                speak(result)
            else:
                speak('Which application should I close?')
            return
        
        elif intent == 'search_google':
            query = entities.get('query', entities.get('search_term', ''))
            if query:
                result = search_google(query)
                speak(result)
            else:
                speak('What should I search for?')
            return
        
        elif intent == 'search_youtube':
            query = entities.get('query', entities.get('search_term', entities.get('search_query', '')))
            if query:
                result = search_youtube(query)
                print(result)
                speak(result)
            else:
                speak('What should I search on YouTube?')
            return
        
        elif 'send' in intent or 'message' in intent or 'whatsapp' in intent:
            contact = entities.get('contact', '')
            message = entities.get('message', '')
            print(f"DEBUG: Intent matched - {intent}")
            print(f"DEBUG: Contact - {contact}")
            print(f"DEBUG: Message - {message}")
            if contact and message:
                print(f"Sending WhatsApp message to {contact}: {message}")
                try:
                    print("DEBUG: Initializing web automation...")
                    from web_automation import WebAutomation
                    print("DEBUG: Creating WebAutomation instance...")
                    bot = WebAutomation()
                    if not bot.driver:
                        speak("Chrome failed to start")
                        return
                    print("DEBUG: Calling whatsapp_send_message...")
                    result = bot.whatsapp_send_message(contact, message)
                    print(f"DEBUG: Result - {result}")
                    speak(result)
                except Exception as e:
                    print(f"WhatsApp error: {e}")
                    import traceback
                    traceback.print_exc()
                    speak("Sorry, WhatsApp messaging failed")
            else:
                speak('Who should I send the message to?')
            return
        
        elif intent == 'time_query':
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
            return
        
        elif intent == 'system_info':
            cpu()
            return
        
        elif intent == 'joke':
            joke()
            return
        
        elif intent == 'weather_query':
            weather()
            return
        
        elif intent == 'screenshot':
            screenshot()
            return
        
        elif 'email' in intent or 'mail' in intent:
            recipient = entities.get('recipient', entities.get('to', ''))
            subject = entities.get('subject', '')
            body = entities.get('body', entities.get('message', ''))
            print(f"DEBUG: Email intent - Recipient: {recipient}, Subject: {subject}")
            
            if not recipient:
                speak('What is the email address?')
                recipient = takeCommand()
            if not subject:
                speak('What is the subject?')
                subject = takeCommand()
            if not body:
                speak('What should I write in the email?')
                body = takeCommand()
            
            try:
                from gmail_service import send_gmail_api
                result = send_gmail_api(recipient, subject, body)
                print(result)
                speak(result)
            except Exception as e:
                print(f"Gmail API error: {e}")
                speak("Sorry, email sending failed")
            return
        
        elif intent == 'shutdown':
            speak('Shutting down the system')
            if platform == "win32":
                os.system('shutdown /p /f')
            return
        
        elif intent == 'other':
            speak('I understand you want to chat, but I\'m focused on task automation. How can I help you with system tasks?')
            return

        elif 'dictionary' in intent or 'translate' in intent:
            word = entities.get('word', entities.get('query', ''))
            if not word:
                speak('What do you want to search in your intelligent dictionary?')
                word = takeCommand()
            translate(word)
            return

        elif 'news' in intent:
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
            return
        
        # Fallback for unhandled intents
        speak('I understand you want to chat, but I\'m focused on task automation. How can I help you with system tasks?')


def wakeUpJARVIS():
    bot_ = Jarvis()
    bot_.wishMe()
    try:
        while True:
            query = takeCommand().lower()
            if query != 'none':
                bot_.execute_query(query)
    except KeyboardInterrupt:
        speak("Goodbye Sir, shutting down JARVIS")
        sys.exit(0)

def jarvis_with_wake_word():
    """JARVIS with wake word activation and keyboard input"""
    import keyboard
    import threading
    
    speak("JARVIS initialized. Say 'Jarvis' to wake me up or press Ctrl+K to type command.")
    bot_ = Jarvis()
    
    # Simple wake word detection
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
    
    def keyboard_listener():
        """Listen for Ctrl+K keyboard shortcut"""
        while True:
            try:
                if keyboard.is_pressed('ctrl+k'):
                    print("\n🎯 Keyboard input mode activated")
                    speak("Type your command")
                    command = input("Enter command: ").strip()
                    if command:
                        print(f"Executing: {command}")
                        bot_.execute_query(command)
                    time.sleep(0.5)  # Prevent multiple triggers
            except:
                pass
            time.sleep(0.1)
    
    # Start keyboard listener in background
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()
    
    while True:
        try:
            print("Listening for 'Jarvis' or press Ctrl+K...")
            with mic as source:
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
            
            text = r.recognize_google(audio, language='en-in').lower()
            print(f"Heard: {text}")
            
            if 'jarvis' in text:
                speak("At your service sir")
                query = takeCommand().lower()
                if query != 'none':
                    bot_.execute_query(query)
            else:
                # If no 'jarvis' but got valid speech, treat as direct command
                if text and text != 'none' and len(text) > 2:
                    print(f"Direct command: {text}")
                    bot_.execute_query(text)
                    
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            pass
        except KeyboardInterrupt:
            speak("Goodbye Sir, shutting down JARVIS")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)


if __name__ == '__main__':
    import time
    
    print("Choose activation method:")
    print("1. Wake word + keyboard (say 'Jarvis' or press Ctrl+K)")
    print("2. Face recognition + wake word + keyboard")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == '1':
        jarvis_with_wake_word()
    else:
        speak("Starting face recognition...")
        jarvis_with_wake_word()  # Skip face recognition for now, go straight to wake word

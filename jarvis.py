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

        # System status on startup
        cpu()
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
        # Use AI only for complex commands
        if any(word in query.lower() for word in ['search', 'youtube', 'gmail', 'email', 'mail', 'whatsapp']):
            try:
                ai_intent = get_ai_intent(query)
                print(f"AI Intent: {ai_intent}")
                if ai_intent['confidence'] > 0.5:
                    self.handle_ai_intent(ai_intent)
                    return
            except Exception as e:
                print(f"AI processing failed: {e}")
        
        # Direct command processing
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

        elif 'cpu' in query or 'battery' in query:
            cpu()
            return

        elif 'joke' in query:
            joke()
            return

        elif 'screenshot' in query:
            speak("taking screenshot")
            screenshot()
            return

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
                youtube(search_term)
                speak(f"Opening YouTube search for {search_term}")
            else:
                speak('What do you want to search on Youtube?')
                search_term = takeCommand()
                if search_term != 'None':
                    youtube(search_term)
                    speak(f"Opening YouTube search for {search_term}")
            return

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
            return

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
            return

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
            speak('I was created by my AI master in 2025')

        elif 'stands for' in query:
            speak('J.A.R.V.I.S stands for JUST A RATHER VERY INTELLIGENT SYSTEM')

        elif 'open' in query and 'code' not in query:
            item = query.replace('open', '').replace('folder', '').strip()
            if 'download' in item:
                item = 'downloads'
            elif item == 'settings':
                os.system('start ms-settings:')
                speak('Opening Windows Settings')
                return
            result = open_anything(item)
            print(result)
            speak(result)
            return
        
        elif 'close' in query:
            item = query.replace('close', '').strip()
            result = close_anything(item)
            speak(result)
            return
        
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

        elif 'sleep' in query or 'exit' in query or 'quit' in query or 'goodbye' in query or 'bye' in query:
            try:
                close_web_automation()
            except:
                pass
            speak("Goodbye Sir, shutting down JARVIS")
            os._exit(0)
    
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
        
        elif intent == 'close_app' or intent == 'close':
            app = entities.get('app', entities.get('application', ''))
            if app:
                result = close_anything(app)
                speak(result)
            else:
                speak('Which application should I close?')
            return
        
        elif intent == 'search' or intent == 'search_google':
            query = entities.get('query', entities.get('search_term', ''))
            if query:
                if entities.get('platform') == 'youtube':
                    result = search_youtube(query)
                    speak(f"Searching YouTube for {query}")
                else:
                    result = search_google(query)
                    speak(f"Searching Google for {query}")
            else:
                speak('What should I search for?')
            return
        
        elif intent == 'search_youtube':
            query = entities.get('query', entities.get('search_term', entities.get('search_query', '')))
            if query:
                youtube(query)
                speak(f"Opening YouTube search for {query}")
            else:
                speak('What should I search on YouTube?')
            return
        
        elif ('send' in intent or 'message' in intent) and 'email' not in intent and 'mail' not in intent and 'whatsapp' in intent:
            contact = entities.get('contact', '')
            message = entities.get('message', '')
            print(f"DEBUG: WhatsApp Intent matched - {intent}")
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
        
        elif intent == 'weather_query' or intent == 'get_weather' or 'weather' in intent or intent == 'check_weather':
            weather()
            return
        
        elif intent == 'check_status' or intent == 'system_status' or 'battery' in str(entities) or 'cpu' in str(entities):
            cpu()
            return
        
        elif intent == 'open' or intent == 'open_app':
            app = entities.get('app', entities.get('application', entities.get('target', '')))
            if app:
                result = open_anything(app)
                speak(result)
            else:
                speak('Which application should I open?')
            return
        
        elif intent == 'screenshot':
            screenshot()
            return
        
        elif any(word in intent.lower() for word in ['email', 'mail', 'gmail']) or any(word in str(entities).lower() for word in ['email', 'mail', 'gmail']) or ('send' in intent and any(word in str(entities).lower() for word in ['mail', 'email', 'gmail'])) or ('write' in intent and any(word in str(entities).lower() for word in ['mail', 'email', 'gmail'])) or ('compose' in intent):
            recipient = entities.get('recipient', entities.get('to', ''))
            subject = entities.get('subject', '')
            body = entities.get('body', entities.get('message', ''))
            print(f"DEBUG: Email intent - Recipient: {recipient}, Subject: {subject}")
            
            # Use OpenAI to draft email if subject provided
            if subject and not body:
                try:
                    import openai
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a professional email assistant. Draft ONLY the email body content (no subject line, no 'Subject:' prefix). Start directly with the greeting."},
                            {"role": "user", "content": f"Write the email body content for: {subject}"}
                        ],
                        max_tokens=200,
                        temperature=0.7
                    )
                    body = response.choices[0].message.content.strip()
                    
                    # Remove subject line if AI included it
                    if body.startswith('Subject:'):
                        lines = body.split('\n')
                        body = '\n'.join(lines[1:]).strip()
                    
                    # Remove any remaining subject references
                    body = body.replace(f'Subject: {subject}', '').strip()
                    print(f"AI drafted email: {body}")
                except Exception as e:
                    print(f"AI drafting failed: {e}")
                    body = f"Dear Sir/Madam,\n\nI am writing regarding {subject}.\n\nThank you for your consideration.\n\nBest regards"
            
            # Use Gmail API to send email directly
            try:
                from gmail_service import send_gmail_api
                
                # Open Gmail draft with URL method (more reliable)
                import urllib.parse
                
                # Clean up body formatting
                if body:
                    body = body.replace("[Your Name]", "Admin")
                    body = body.replace("[Recipient's Name]", "")
                    if not any(word in body for word in ["Best regards", "Regards", "Sincerely"]):
                        body += "\n\nBest regards,\nAdmin"
                
                # URL encode for Gmail
                subject_encoded = urllib.parse.quote(subject or "Email from JARVIS")
                body_encoded = urllib.parse.quote(body or "").replace("%0A", "%0D%0A")
                
                # Create Gmail compose URL (recipient left blank)
                gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject_encoded}&body={body_encoded}"
                
                # Open Gmail draft
                import webbrowser
                webbrowser.open(gmail_url)
                speak(f"Gmail draft opened with subject: {subject}. Please add recipient and send.")
                
            except Exception as e:
                print(f"Gmail API error: {e}")
                # Fallback to web interface
                try:
                    from web_automation import init_web_automation
                    bot = init_web_automation()
                    result = bot.gmail_compose(recipient or 'recipient@example.com', subject, body)
                    speak(f"Gmail opened with drafted email: {subject}")
                except Exception as web_error:
                    print(f"Web automation error: {web_error}")
                    speak("Opening Gmail manually")
                    import webbrowser
                    webbrowser.open("https://mail.google.com")
            return
        
        elif intent == 'shutdown':
            speak('Shutting down the system')
            if platform == "win32":
                os.system('shutdown /p /f')
            return
        
        elif intent == 'create' and 'painting' in str(entities):
            # Handle "paints" as close paint app
            result = close_anything('paint')
            speak(result)
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
    import time
    
    speak("JARVIS initialized. Say 'Jarvis' or press Ctrl+K for commands.")
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
            print("Listening for 'Jarvis' or Ctrl+K...")
            with mic as source:
                audio = r.listen(source, timeout=0.5, phrase_time_limit=2)
            
            text = r.recognize_google(audio, language='en-in').lower()
            print(f"Heard: {text}")
            
            if 'jarvis' in text:
                speak("At your service sir")
                print("Listening for command...")
                query = takeCommand()
                if query and query != 'none' and query.strip():
                    print(f"Processing command: {query}")
                    bot_.execute_query(query.lower())
                else:
                    print("No command received, continuing...")
            else:
                # If no 'jarvis' but got valid speech, treat as direct command
                if text and text != 'none' and len(text) > 2:
                    print(f"Direct command: {text}")
                    bot_.execute_query(text)
                    
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            pass
        except KeyboardInterrupt:
            print("\nShutting down JARVIS...")
            speak("Goodbye Sir, shutting down JARVIS")
            os._exit(0)
        except KeyboardInterrupt:
            print("\nShutting down JARVIS...")
            os._exit(0)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)


if __name__ == '__main__':
    bot = Jarvis()
    bot.wishMe()
    jarvis_with_wake_word()

import speech_recognition as sr
import pyttsx3
import threading
import time

class WakeWordDetector:
    def __init__(self, wake_word="jarvis"):
        self.wake_word = wake_word.lower()
        self.listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize TTS
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def speak(self, text):
        """Text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=2)
                
                text = self.recognizer.recognize_google(audio, language='en-in').lower()
                
                if self.wake_word in text:
                    return True
                    
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                pass
            except Exception:
                time.sleep(0.1)
    
    def start_listening(self):
        """Start wake word detection in background"""
        self.listening = True
        thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        thread.start()
        return thread

def wait_for_wake_word():
    """Wait for wake word and return True when detected"""
    detector = WakeWordDetector("jarvis")
    if detector.listen_for_wake_word():
        detector.speak("How can I help you?")
        return True
    return False
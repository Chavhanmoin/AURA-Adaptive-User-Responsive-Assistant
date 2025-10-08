"""
Speech Engine Module for AURA Assistant
Handles voice recognition, wake word detection, and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import pvporcupine
import pyaudio
import struct
import logging
import threading
import time

class SpeechEngine:
    """Handles all speech-related functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.porcupine = None
        self.audio_stream = None
        self.setup_components()
    
    def setup_components(self):
        """Initialize speech components"""
        try:
            # Setup TTS
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)
            
            # Setup wake word detection (Porcupine)
            self.porcupine = pvporcupine.create(
                access_key="YOUR_PICOVOICE_ACCESS_KEY",  # Replace with actual key
                keywords=["hey google"]  # Using built-in keyword, replace with custom "hey aura"
            )
            
            # Setup audio stream for wake word
            self.audio_stream = pyaudio.PyAudio().open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            # Calibrate microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                
            self.logger.info("Speech engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize speech engine: {e}")
            # Fallback without wake word detection
            self.porcupine = None
    
    def detect_wake_word(self):
        """Detect wake word using Porcupine"""
        if not self.porcupine or not self.audio_stream:
            # Fallback: simple voice activity detection
            return self.simple_wake_detection()
        
        try:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            
            keyword_index = self.porcupine.process(pcm)
            return keyword_index >= 0
            
        except Exception as e:
            self.logger.error(f"Wake word detection error: {e}")
            return False
    
    def simple_wake_detection(self):
        """Simple fallback wake word detection"""
        try:
            with self.microphone as source:
                self.logger.info("Listening for voice...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
            text = self.recognizer.recognize_google(audio).lower()
            return "hey aura" in text or "aura" in text
            
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except Exception as e:
            self.logger.error(f"Simple wake detection error: {e}")
            return False
    
    def listen_for_command(self, timeout=5):
        """Listen for voice command after wake word"""
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            command = self.recognizer.recognize_google(audio)
            self.logger.info(f"Recognized: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            self.logger.warning("No command received within timeout")
            return None
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return None
        except Exception as e:
            self.logger.error(f"Command recognition error: {e}")
            return None
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            self.logger.info(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.audio_stream:
                self.audio_stream.close()
            if self.porcupine:
                self.porcupine.delete()
                
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
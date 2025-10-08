#!/usr/bin/env python3
"""
Hybrid A.U.R.A Assistant - Main Entry Point
AI + Automation + IoT System

Author: AURA Development Team
Version: 1.0.0
"""

import os
import sys
import time
import threading
import logging
from pathlib import Path

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.speech_engine import SpeechEngine
from modules.command_handler import CommandHandler
from modules.ai_response import AIResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/aura.log'),
        logging.StreamHandler()
    ]
)

class AURAAssistant:
    """Main AURA Assistant Class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.speech_engine = None
        self.command_handler = None
        self.ai_response = None
        
    def initialize(self):
        """Initialize all components"""
        try:
            self.logger.info("Initializing AURA Assistant...")
            
            # Create data directories
            os.makedirs('data/logs', exist_ok=True)
            
            # Initialize components
            self.speech_engine = SpeechEngine()
            self.command_handler = CommandHandler()
            self.ai_response = AIResponse()
            
            self.logger.info("AURA Assistant initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AURA: {e}")
            return False
    
    def listen_for_wake_word(self):
        """Listen for wake word 'Hey Aura'"""
        self.logger.info("Listening for wake word...")
        
        while self.running:
            try:
                if self.speech_engine.detect_wake_word():
                    self.logger.info("Wake word detected!")
                    self.speech_engine.speak("Yes, how can I help you?")
                    self.process_command()
                    
            except Exception as e:
                self.logger.error(f"Error in wake word detection: {e}")
                time.sleep(1)
    
    def process_command(self):
        """Process voice command after wake word"""
        try:
            command = self.speech_engine.listen_for_command()
            if command:
                self.logger.info(f"Command received: {command}")
                response = self.command_handler.handle_command(command)
                
                if response:
                    self.speech_engine.speak(response)
                    
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            self.speech_engine.speak("Sorry, I couldn't process that command.")
    
    def start(self):
        """Start the AURA Assistant"""
        if not self.initialize():
            return False
            
        self.running = True
        self.logger.info("AURA Assistant started")
        self.speech_engine.speak("AURA Assistant is now active")
        
        try:
            # Start wake word detection in main thread
            self.listen_for_wake_word()
            
        except KeyboardInterrupt:
            self.logger.info("Shutdown requested by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the AURA Assistant"""
        self.running = False
        self.logger.info("AURA Assistant stopped")
        self.speech_engine.speak("AURA Assistant is shutting down")

def main():
    """Main function"""
    aura = AURAAssistant()
    aura.start()

if __name__ == "__main__":
    main()
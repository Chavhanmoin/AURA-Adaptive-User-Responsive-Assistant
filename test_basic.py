#!/usr/bin/env python3
"""
Basic AURA Test Script
Test core functionality without advanced features
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def test_imports():
    """Test if core modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import pyttsx3
        print("✓ pyttsx3 (Text-to-Speech)")
        
        import requests
        print("✓ requests")
        
        import json
        print("✓ json")
        
        # Test optional imports
        try:
            import speech_recognition as sr
            print("✓ speech_recognition")
        except ImportError:
            print("✗ speech_recognition (install with: pip install SpeechRecognition)")
        
        try:
            import selenium
            print("✓ selenium")
        except ImportError:
            print("✗ selenium (install with: pip install selenium)")
        
        try:
            import openai
            print("✓ openai")
        except ImportError:
            print("✗ openai (install with: pip install openai)")
        
        print("\nCore modules test completed!")
        return True
        
    except Exception as e:
        print(f"Import test failed: {e}")
        return False

def test_tts():
    """Test text-to-speech functionality"""
    try:
        print("\nTesting Text-to-Speech...")
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)
        
        print("Speaking test message...")
        engine.say("AURA Assistant test successful")
        engine.runAndWait()
        
        print("✓ Text-to-Speech working")
        return True
        
    except Exception as e:
        print(f"✗ TTS test failed: {e}")
        return False

def main():
    """Run basic tests"""
    print("AURA Assistant - Basic Functionality Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        return
    
    # Test TTS
    test_tts()
    
    print("\nBasic test completed!")
    print("If all tests pass, you can run: python start_aura.py")

if __name__ == "__main__":
    main()
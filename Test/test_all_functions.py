#!/usr/bin/env python3
"""Comprehensive test script for all J.A.R.V.I.S functions"""

import sys
import traceback

def test_helpers():
    """Test helper functions"""
    print("=== Testing Helper Functions ===")
    
    try:
        from helpers import speak, cpu, weather, joke, screenshot
        
        print("✓ Testing speak function...")
        speak("Testing J.A.R.V.I.S speech system")
        
        print("✓ Testing CPU function...")
        cpu()
        
        print("✓ Testing weather function...")
        weather()
        
        print("✓ Testing joke function...")
        joke()
        
        print("✓ Testing screenshot function...")
        screenshot()
        
        print("✓ All helper functions tested successfully!")
        
    except Exception as e:
        print(f"✗ Error in helpers: {e}")
        traceback.print_exc()

def test_news():
    """Test news functions"""
    print("\n=== Testing News Functions ===")
    
    try:
        from news import speak_news, getNewsUrl
        
        print("✓ Testing news URL function...")
        url = getNewsUrl()
        print(f"News URL: {url}")
        
        print("✓ Testing speak news function...")
        speak_news()
        
        print("✓ News functions tested successfully!")
        
    except Exception as e:
        print(f"✗ Error in news: {e}")
        traceback.print_exc()

def test_youtube():
    """Test YouTube functions"""
    print("\n=== Testing YouTube Functions ===")
    
    try:
        from youtube import youtube
        
        print("✓ Testing YouTube search...")
        youtube("test search")
        
        print("✓ YouTube functions tested successfully!")
        
    except Exception as e:
        print(f"✗ Error in YouTube: {e}")
        traceback.print_exc()

def test_dictionary():
    """Test dictionary functions"""
    print("\n=== Testing Dictionary Functions ===")
    
    try:
        from diction import translate
        
        print("✓ Testing dictionary translate...")
        translate("hello")
        
        print("✓ Dictionary functions tested successfully!")
        
    except Exception as e:
        print(f"✗ Error in dictionary: {e}")
        traceback.print_exc()

def test_ocr():
    """Test OCR functions"""
    print("\n=== Testing OCR Functions ===")
    
    try:
        from OCR import OCR
        
        print("✓ Testing OCR function...")
        print("Note: OCR requires camera - test manually if needed")
        
        print("✓ OCR functions loaded successfully!")
        
    except Exception as e:
        print(f"✗ Error in OCR: {e}")
        traceback.print_exc()

def test_jarvis_main():
    """Test main JARVIS class"""
    print("\n=== Testing Main JARVIS Class ===")
    
    try:
        from jarvis import Jarvis
        
        print("✓ Testing JARVIS initialization...")
        bot = Jarvis()
        
        print("✓ Testing sample queries...")
        test_queries = [
            "what is the time",
            "tell me a joke",
            "what is my cpu usage"
        ]
        
        for query in test_queries:
            print(f"Testing query: {query}")
            bot.execute_query(query)
        
        print("✓ JARVIS main class tested successfully!")
        
    except Exception as e:
        print(f"✗ Error in main JARVIS: {e}")
        traceback.print_exc()

def main():
    """Run all tests"""
    print("J.A.R.V.I.S Function Test Suite")
    print("=" * 40)
    
    test_helpers()
    test_news()
    test_youtube()
    test_dictionary()
    test_ocr()
    test_jarvis_main()
    
    print("\n" + "=" * 40)
    print("Test suite completed!")

if __name__ == "__main__":
    main()
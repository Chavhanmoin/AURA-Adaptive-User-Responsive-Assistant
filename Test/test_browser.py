#!/usr/bin/env python3
"""Simple test for browser automation"""

import webbrowser
import time

def test_browser():
    print("Testing browser automation...")
    
    # Test default browser
    print("Opening Google in default browser...")
    webbrowser.open('https://google.com')
    time.sleep(2)
    
    print("Opening YouTube in default browser...")
    webbrowser.open('https://youtube.com')
    time.sleep(2)
    
    print("Browser test completed!")

if __name__ == "__main__":
    test_browser()
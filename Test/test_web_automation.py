#!/usr/bin/env python3
"""Test web automation functionality"""

import time
import webbrowser
from sys import platform

def setup_browser():
    """Setup Chrome browser"""
    if platform == "win32":
        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    try:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        return True
    except:
        print("Chrome not found, using default browser")
        return False

def test_web_automation():
    """Test all web automation features"""
    
    print("=== Testing Web Automation ===")
    setup_browser()
    
    # Test basic website opening
    print("\n1. Testing website opening:")
    sites = [
        ("Google", "https://google.com"),
        ("YouTube", "https://youtube.com"),
        ("Amazon", "https://amazon.com"),
        ("GitHub", "https://github.com"),
        ("StackOverflow", "https://stackoverflow.com")
    ]
    
    for name, url in sites:
        print(f"Opening {name}...")
        try:
            webbrowser.get('chrome').open_new_tab(url)
        except:
            webbrowser.open_new_tab(url)
        time.sleep(2)
    
    # Test search functionality
    print("\n2. Testing search automation:")
    searches = ["python tutorial", "AI assistant", "web automation"]
    
    for search in searches:
        print(f"Searching for: {search}")
        url = f'https://google.com/search?q={search}'
        try:
            webbrowser.get('chrome').open_new_tab(url)
        except:
            webbrowser.open_new_tab(url)
        time.sleep(2)
    
    # Test YouTube search
    print("\n3. Testing YouTube search:")
    from youtube import youtube
    
    yt_searches = ["machine learning", "python programming", "web development"]
    for search in yt_searches:
        print(f"YouTube search: {search}")
        youtube(search)
        time.sleep(2)
    
    # Test location search
    print("\n4. Testing location search:")
    locations = ["New York", "London", "Tokyo"]
    
    for location in locations:
        print(f"Opening map for: {location}")
        url = f'https://google.nl/maps/place/{location}'
        try:
            webbrowser.get('chrome').open_new_tab(url)
        except:
            webbrowser.open_new_tab(url)
        time.sleep(2)
    
    print("\n=== Web automation tests completed! ===")

if __name__ == "__main__":
    test_web_automation()
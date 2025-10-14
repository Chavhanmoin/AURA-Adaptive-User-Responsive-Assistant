#!/usr/bin/env python3
"""Test Selenium web automation functionality"""

from web_automation import WebAutomation
import time

def test_selenium_automation():
    """Test all Selenium automation features"""
    
    print("=== Testing Selenium Web Automation ===")
    
    # Initialize web automation
    bot = WebAutomation()
    
    if not bot.driver:
        print("❌ Failed to initialize Chrome driver")
        return
    
    print("✅ Chrome driver initialized successfully")
    
    # Test Google search
    print("\n1. Testing Google search...")
    result = bot.google_search("python selenium tutorial")
    print(f"Result: {result}")
    time.sleep(3)
    
    # Test YouTube search
    print("\n2. Testing YouTube search...")
    result = bot.youtube_search("AI assistant tutorial")
    print(f"Result: {result}")
    time.sleep(5)
    
    # Test navigation
    print("\n3. Testing website navigation...")
    bot.driver.get("https://github.com")
    print("✅ Navigated to GitHub")
    time.sleep(2)
    
    bot.driver.get("https://stackoverflow.com")
    print("✅ Navigated to StackOverflow")
    time.sleep(2)
    
    # Test form interaction
    print("\n4. Testing form interaction...")
    try:
        bot.driver.get("https://www.google.com")
        search_box = bot.driver.find_element("name", "q")
        search_box.send_keys("selenium automation test")
        print("✅ Form interaction successful")
    except Exception as e:
        print(f"❌ Form interaction failed: {e}")
    
    time.sleep(2)
    
    print("\n5. Manual tests (require user interaction):")
    print("- WhatsApp: Requires QR code scan")
    print("- Gmail: Requires login")
    
    # Close browser
    print("\n6. Closing browser...")
    bot.close_browser()
    print("✅ Browser closed successfully")
    
    print("\n=== Selenium automation tests completed! ===")

if __name__ == "__main__":
    test_selenium_automation()
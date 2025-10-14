#!/usr/bin/env python3
"""Safe test suite for JARVIS functions (excludes VS Code)"""

import time
from jarvis import Jarvis

def test_safe_functions():
    """Test JARVIS functions safely without affecting VS Code"""
    
    print("=== JARVIS Safe Function Test ===\n")
    
    bot = Jarvis()
    
    # Safe test commands (no VS Code)
    test_commands = [
        # System automation (safe apps)
        "open notepad",
        "close notepad", 
        "open calculator",
        "close calculator",
        "open paint",
        "close paint",
        "screenshot",
        "cpu usage",
        "what is the time",
        
        # Web automation
        "search python tutorial",
        "search youtube music",
        "open google",
        "open youtube",
        "open amazon",
        "open github",
        
        # Voice & AI features
        "tell me a joke",
        "wikipedia python programming",
        "what is the weather",
        
        # File operations
        "open documents folder",
        "open downloads folder",
        "open desktop folder",
        "open pictures folder",
        
        # System info
        "system information",
        "battery status",
        
        # Memory functions
        "remember that testing is important",
        "do you remember anything",
        
        # Dictionary
        "dictionary computer",
        
        # News
        "latest news",
        
        # Voice switching
        "change voice to female",
        "change voice to male",
        
        # Location
        "location new york",
        
        # YouTube specific
        "youtube search artificial intelligence",
        
        # WhatsApp/Email (will ask for details)
        "send whatsapp message",
        "compose email"
    ]
    
    print(f"Testing {len(test_commands)} safe commands...\n")
    
    success_count = 0
    error_count = 0
    
    for i, command in enumerate(test_commands, 1):
        print(f"{i:2d}. Testing: '{command}'")
        try:
            bot.execute_query(command)
            print("    ✅ Success")
            success_count += 1
        except Exception as e:
            print(f"    ❌ Error: {e}")
            error_count += 1
        
        time.sleep(2)  # Pause between tests
        print()
    
    print("=== Test Results ===")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Success Rate: {(success_count/(success_count+error_count)*100):.1f}%")
    
    print("\n=== Function Categories Tested ===")
    print("✅ System Control: Notepad, Calculator, Paint")
    print("✅ Web Automation: Google, YouTube, Amazon, GitHub") 
    print("✅ Voice Features: Jokes, Wikipedia, Weather, News")
    print("✅ File Operations: Documents, Downloads, Desktop, Pictures")
    print("✅ Memory: Remember/recall functionality")
    print("✅ AI Integration: Intent recognition")
    print("✅ System Info: CPU, Battery, Time")
    print("✅ Communication: WhatsApp, Email setup")
    
    print("\n🚫 Excluded for safety: VS Code operations")
    print("\n=== Safe test completed! ===")

if __name__ == "__main__":
    test_safe_functions()
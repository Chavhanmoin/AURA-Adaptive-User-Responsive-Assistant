#!/usr/bin/env python3
"""
JARVIS Command Tester
Automatically tests all JARVIS commands without voice input
"""

import time
import sys
import os

# Add current directory to path to import jarvis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import Jarvis

def test_commands():
    """Test all JARVIS commands programmatically"""
    
    # Initialize JARVIS
    bot = Jarvis()
    
    # Test commands list
    commands = [
        # System Control
        ("System Control", [
            "open notepad",
            "close notepad", 
            "open calculator",
            "take screenshot",
            "cpu usage",
            "battery status"
        ]),
        
        # Web Automation  
        ("Web Automation", [
            "search python tutorials",
            "youtube search machine learning",
            "open google",
            "search for AI news"
        ]),
        
        # Information & Utilities
        ("Information & Utilities", [
            "what is the time",
            "tell me a joke",
            "what's the weather"
        ]),
        
        # File Operations
        ("File Operations", [
            "open downloads",
            "open documents", 
            "open desktop"
        ]),
        
        # Quick Tests
        ("Quick Tests", [
            "jarvis are you there",
            "your name",
            "open settings"
        ])
    ]
    
    print("🤖 Starting JARVIS Command Test Suite")
    print("=" * 50)
    
    total_tests = 0
    passed_tests = 0
    
    for category, test_list in commands:
        print(f"\n📂 Testing {category}")
        print("-" * 30)
        
        for command in test_list:
            total_tests += 1
            print(f"🧪 Testing: '{command}'")
            
            try:
                # Execute command
                bot.execute_query(command)
                print("✅ PASSED")
                passed_tests += 1
                
            except Exception as e:
                print(f"❌ FAILED: {e}")
            
            # Small delay between commands
            time.sleep(1)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Total Commands: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests, total_tests

if __name__ == "__main__":
    try:
        passed, total = test_commands()
        print(f"\n🎯 Testing complete: {passed}/{total} commands working")
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Testing failed: {e}")
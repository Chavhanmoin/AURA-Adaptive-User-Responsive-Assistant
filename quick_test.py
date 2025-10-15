#!/usr/bin/env python3
"""
Quick JARVIS Test Script
Tests core functionality without voice input
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import Jarvis

def quick_test():
    """Test essential JARVIS commands"""
    
    bot = Jarvis()
    
    # Essential test commands
    tests = [
        "search python tutorials",
        "youtube search AI",
        "open youtube"
    ]
    
    print("🚀 Quick JARVIS Test")
    print("=" * 30)
    
    for i, cmd in enumerate(tests, 1):
        print(f"\n{i}. Testing: '{cmd}'")
        try:
            bot.execute_query(cmd)
            print("✅ OK")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 Test Complete!")

if __name__ == "__main__":
    quick_test()
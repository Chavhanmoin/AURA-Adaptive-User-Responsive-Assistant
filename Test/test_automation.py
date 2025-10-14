#!/usr/bin/env python3
"""Test script for J.A.R.V.I.S system automation features"""

import sys
import traceback
import time

def test_system_monitoring():
    """Test system monitoring functions"""
    print("=== Testing System Monitoring ===")
    
    try:
        from helpers import cpu, screenshot
        
        print("✓ Testing CPU and battery monitoring...")
        cpu()
        
        print("✓ Testing screenshot capture...")
        screenshot()
        print("Screenshot saved to C:\\Users\\Admin\\Pictures\\Screenshots\\")
        
        print("✓ System monitoring tests passed!")
        
    except Exception as e:
        print(f"✗ Error in system monitoring: {e}")
        traceback.print_exc()

def test_web_automation():
    """Test web browser automation"""
    print("\n=== Testing Web Automation ===")
    
    try:
        from jarvis import Jarvis
        
        bot = Jarvis()
        
        print("✓ Testing website opening...")
        test_queries = [
            "open google",
            "open youtube", 
            "search youtube",
            "open stackoverflow"
        ]
        
        for query in test_queries:
            print(f"Testing: {query}")
            bot.execute_query(query)
            time.sleep(1)
        
        print("✓ Web automation tests passed!")
        
    except Exception as e:
        print(f"✗ Error in web automation: {e}")
        traceback.print_exc()

def test_file_operations():
    """Test file and application operations"""
    print("\n=== Testing File Operations ===")
    
    try:
        from jarvis import Jarvis
        
        bot = Jarvis()
        
        print("✓ Testing file operations...")
        test_queries = [
            "remember that testing jarvis automation",
            "do you remember anything",
            "open code"
        ]
        
        for query in test_queries:
            print(f"Testing: {query}")
            bot.execute_query(query)
            time.sleep(1)
        
        print("✓ File operations tests passed!")
        
    except Exception as e:
        print(f"✗ Error in file operations: {e}")
        traceback.print_exc()

def test_system_commands():
    """Test system-level commands"""
    print("\n=== Testing System Commands ===")
    
    try:
        from jarvis import Jarvis
        
        bot = Jarvis()
        
        print("✓ Testing system information...")
        test_queries = [
            "cpu",
            "the time",
            "your name",
            "your master"
        ]
        
        for query in test_queries:
            print(f"Testing: {query}")
            bot.execute_query(query)
            time.sleep(1)
        
        print("✓ System commands tests passed!")
        
    except Exception as e:
        print(f"✗ Error in system commands: {e}")
        traceback.print_exc()

def test_voice_switching():
    """Test voice switching automation"""
    print("\n=== Testing Voice Switching ===")
    
    try:
        from jarvis import Jarvis
        
        bot = Jarvis()
        
        print("✓ Testing voice switching...")
        test_queries = [
            "voice female",
            "voice male"
        ]
        
        for query in test_queries:
            print(f"Testing: {query}")
            bot.execute_query(query)
            time.sleep(2)
        
        print("✓ Voice switching tests passed!")
        
    except Exception as e:
        print(f"✗ Error in voice switching: {e}")
        traceback.print_exc()

def main():
    """Run all automation tests"""
    print("J.A.R.V.I.S System Automation Test Suite")
    print("=" * 45)
    
    test_system_monitoring()
    test_web_automation()
    test_file_operations()
    test_system_commands()
    test_voice_switching()
    
    print("\n" + "=" * 45)
    print("Automation test suite completed!")
    print("\nNote: Some tests open browsers/applications.")
    print("Close them manually if needed.")

if __name__ == "__main__":
    main()
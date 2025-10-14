#!/usr/bin/env python3
"""Test system control functionality"""

from system_control import open_anything, close_anything, execute_system_command
import time

def test_system_control():
    """Test all system control functions"""
    
    print("=== Testing System Control ===")
    
    # Test opening applications
    print("\n1. Testing application opening:")
    apps = ["notepad", "calc", "mspaint"]
    for app in apps:
        result = open_anything(app)
        print(f"Open {app}: {result}")
        time.sleep(1)
    
    # Test closing applications
    print("\n2. Testing application closing:")
    for app in apps:
        result = close_anything(app)
        print(f"Close {app}: {result}")
        time.sleep(1)
    
    # Test file/folder operations
    print("\n3. Testing file/folder opening:")
    paths = ["Documents", "Desktop", "Downloads"]
    for path in paths:
        result = open_anything(path)
        print(f"Open {path}: {result}")
        time.sleep(1)
    
    # Test system commands
    print("\n4. Testing system commands:")
    commands = ["dir", "ipconfig", "systeminfo"]
    for cmd in commands:
        result = execute_system_command(cmd)
        print(f"Execute {cmd}: Command completed")
        time.sleep(1)
    
    print("\n=== All tests completed! ===")

if __name__ == "__main__":
    test_system_control()
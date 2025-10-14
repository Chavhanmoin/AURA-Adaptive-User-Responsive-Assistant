#!/usr/bin/env python3
"""Test script for JARVIS helper functions"""

from helpers import speak, cpu, weather

def test_basic_functions():
    """Test basic JARVIS functions"""
    print("Testing speak function...")
    speak("Hello, JARVIS is working!")
    
    print("Testing CPU function...")
    cpu()
    
    print("Testing weather function...")
    weather()

if __name__ == "__main__":
    test_basic_functions()
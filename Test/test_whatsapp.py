#!/usr/bin/env python3
"""Test WhatsApp automation"""

from web_automation import send_whatsapp_message

def test_whatsapp():
    """Test WhatsApp message sending"""
    
    print("=== WhatsApp Test ===")
    print("This will:")
    print("1. Open WhatsApp Web")
    print("2. Ask you to scan QR code (if not logged in)")
    print("3. Send a test message")
    
    contact = input("Enter contact name: ")
    message = input("Enter message: ")
    
    print(f"Sending '{message}' to {contact}...")
    result = send_whatsapp_message(contact, message)
    print(result)

if __name__ == "__main__":
    test_whatsapp()
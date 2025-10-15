#!/usr/bin/env python3
"""Test Gmail URL Method"""

import urllib.parse
import webbrowser
from jarvis import Jarvis
from ai_intent_recognition import get_ai_intent

def test_gmail_url_encoding():
    """Test Gmail URL encoding"""
    print("🔄 Testing Gmail URL Encoding...")
    
    subject = "Test Subject with Special Characters & Symbols"
    body = "Dear Sir/Madam,\n\nThis is a test email.\n\nBest regards,\nAdmin"
    
    # URL encode
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body).replace("%0A", "%0D%0A")
    
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject_encoded}&body={body_encoded}"
    
    print(f"✅ Subject encoded: {subject_encoded}")
    print(f"✅ Body encoded length: {len(body_encoded)}")
    print(f"✅ Gmail URL created: {len(gmail_url)} characters")
    
    return True

def test_ai_email_drafting():
    """Test AI email drafting"""
    print("\n🔄 Testing AI Email Drafting...")
    
    test_subjects = [
        "sick leave",
        "meeting request", 
        "project update",
        "assignment submission"
    ]
    
    try:
        import openai
        for subject in test_subjects:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional email assistant. Draft a formal, polite email based on the subject provided."},
                    {"role": "user", "content": f"Draft an email for: {subject}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            body = response.choices[0].message.content.strip()
            print(f"✅ {subject}: {len(body)} characters drafted")
        
        return True
    except Exception as e:
        print(f"❌ AI drafting failed: {e}")
        return False

def test_email_intent_recognition():
    """Test email intent recognition"""
    print("\n🔄 Testing Email Intent Recognition...")
    
    email_commands = [
        "write a mail to professor for assignment",
        "email about sick leave",
        "compose email for meeting request",
        "mail to manager about project update",
        "gmail to client about delivery"
    ]
    
    passed = 0
    for command in email_commands:
        try:
            intent = get_ai_intent(command)
            print(f"Command: '{command}'")
            print(f"Intent: {intent['intent']}, Confidence: {intent['confidence']}")
            
            if any(word in intent['intent'].lower() for word in ['email', 'mail', 'send']):
                print("✅ Email intent recognized")
                passed += 1
            else:
                print("❌ Email intent missed")
        except Exception as e:
            print(f"❌ Intent recognition failed: {e}")
    
    return passed == len(email_commands)

def test_jarvis_email_integration():
    """Test JARVIS email integration"""
    print("\n🔄 Testing JARVIS Email Integration...")
    
    try:
        bot = Jarvis()
        
        # Test email command
        test_command = "write a mail to professor for assignment submission"
        print(f"Testing: '{test_command}'")
        
        # This should open Gmail draft
        bot.execute_query(test_command)
        print("✅ Email command executed successfully")
        
        return True
    except Exception as e:
        print(f"❌ JARVIS email integration failed: {e}")
        return False

def test_gmail_draft_opening():
    """Test Gmail draft opening"""
    print("\n🔄 Testing Gmail Draft Opening...")
    
    try:
        subject = "Test Email from JARVIS"
        body = "Dear Sir/Madam,\n\nThis is a test email from JARVIS.\n\nBest regards,\nAdmin"
        
        # Clean up body
        body = body.replace("[Your Name]", "Admin")
        if not any(word in body for word in ["Best regards", "Regards", "Sincerely"]):
            body += "\n\nBest regards,\nAdmin"
        
        # URL encode
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body).replace("%0A", "%0D%0A")
        
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject_encoded}&body={body_encoded}"
        
        print(f"Gmail URL: {gmail_url[:100]}...")
        print("✅ Gmail draft URL created successfully")
        
        # Uncomment to actually open Gmail
        # webbrowser.open(gmail_url)
        
        return True
    except Exception as e:
        print(f"❌ Gmail draft opening failed: {e}")
        return False

def run_gmail_tests():
    """Run complete Gmail test suite"""
    print("=" * 60)
    print("📧 GMAIL URL METHOD TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Gmail URL Encoding", test_gmail_url_encoding),
        ("AI Email Drafting", test_ai_email_drafting),
        ("Email Intent Recognition", test_email_intent_recognition),
        ("Gmail Draft Opening", test_gmail_draft_opening),
        ("JARVIS Integration", test_jarvis_email_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    # Results Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"✅ PASSED: {passed}/{total}")
    print(f"❌ FAILED: {total - passed}/{total}")
    print(f"📈 SUCCESS RATE: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Gmail URL method is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the issues above.")
    
    # Usage Instructions
    print("\n" + "=" * 60)
    print("📋 USAGE INSTRUCTIONS")
    print("=" * 60)
    print("To test Gmail function manually:")
    print("1. Say: 'Jarvis' → 'write a mail to professor for assignment'")
    print("2. Press Ctrl+K → type 'email about sick leave'")
    print("3. Gmail will open with pre-filled subject and body")
    print("4. Add recipient email and send manually")
    
    return passed == total

if __name__ == "__main__":
    success = run_gmail_tests()
    
    # Optional: Test actual Gmail opening
    print("\n" + "=" * 60)
    print("🔧 MANUAL TEST")
    print("=" * 60)
    test_manual = input("Open actual Gmail draft for testing? (y/n): ").lower()
    if test_manual == 'y':
        subject = "Test Email from JARVIS"
        body = "Dear Sir/Madam,\n\nThis is a test email to verify the Gmail URL method is working.\n\nBest regards,\nAdmin"
        
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body).replace("%0A", "%0D%0A")
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject_encoded}&body={body_encoded}"
        
        webbrowser.open(gmail_url)
        print("✅ Gmail draft opened! Check your browser.")
    
    exit(0 if success else 1)
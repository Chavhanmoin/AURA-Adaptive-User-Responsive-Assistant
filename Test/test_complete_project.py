#!/usr/bin/env python3
"""Complete JARVIS Project Test Suite - Bug Detection & Evaluation"""

import sys
import time
import traceback
from jarvis import Jarvis

class JarvisTestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.bot = Jarvis()
    
    def test_function(self, test_name, command):
        """Test individual function and track results"""
        print(f"\n🔄 Testing: {test_name}")
        print(f"   Command: '{command}'")
        
        try:
            self.bot.execute_query(command)
            print(f"   ✅ PASSED")
            self.passed += 1
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")
            self.failed += 1
            self.errors.append({
                'test': test_name,
                'command': command,
                'error': str(e),
                'traceback': traceback.format_exc()
            })
        
        time.sleep(2)  # Pause between tests
    
    def run_complete_test_suite(self):
        """Run comprehensive test suite"""
        
        print("=" * 60)
        print("🤖 JARVIS COMPLETE PROJECT TEST SUITE")
        print("=" * 60)
        
        # System Control Tests
        print("\n📁 SYSTEM CONTROL TESTS")
        print("-" * 30)
        
        system_tests = [
            ("Open Notepad", "open notepad"),
            ("Close Notepad", "close notepad"),
            ("Open Calculator", "open calculator"),
            ("Close Calculator", "close calculator"),
            ("Open Paint", "open paint"),
            ("Close Paint", "close paint"),
            ("Take Screenshot", "screenshot"),
            ("CPU Usage", "cpu usage"),
            ("System Time", "what is the time"),
            ("Open Documents Folder", "open documents folder"),
            ("Open Downloads Folder", "open downloads folder"),
            ("Open Desktop Folder", "open desktop folder"),
        ]
        
        for test_name, command in system_tests:
            self.test_function(test_name, command)
        
        # Web Automation Tests
        print("\n🌐 WEB AUTOMATION TESTS")
        print("-" * 30)
        
        web_tests = [
            ("Google Search", "search python programming"),
            ("YouTube Search", "youtube search artificial intelligence"),
            ("Open Google", "open google"),
            ("Open YouTube", "open youtube"),
            ("Open Amazon", "open amazon"),
            ("Open GitHub", "open github"),
            ("Location Search", "location new york"),
        ]
        
        for test_name, command in web_tests:
            self.test_function(test_name, command)
        
        # AI & Voice Tests
        print("\n🧠 AI & VOICE TESTS")
        print("-" * 30)
        
        ai_tests = [
            ("Tell Joke", "tell me a joke"),
            ("Weather Query", "what is the weather"),
            ("Wikipedia Search", "wikipedia python programming"),
            ("Voice Switch Female", "change voice to female"),
            ("Voice Switch Male", "change voice to male"),
            ("JARVIS Identity", "what is your name"),
            ("JARVIS Purpose", "what do you stand for"),
        ]
        
        for test_name, command in ai_tests:
            self.test_function(test_name, command)
        
        # Communication Tests
        print("\n📱 COMMUNICATION TESTS")
        print("-" * 30)
        
        comm_tests = [
            ("WhatsApp Message", "send whatsapp message to test saying hello"),
            ("Email Compose", "email to test@example.com about meeting"),
            ("News Headlines", "latest news"),
        ]
        
        for test_name, command in comm_tests:
            self.test_function(test_name, command)
        
        # Memory & Utility Tests
        print("\n🧮 MEMORY & UTILITY TESTS")
        print("-" * 30)
        
        utility_tests = [
            ("Remember Something", "remember that testing is important"),
            ("Recall Memory", "do you remember anything"),
            ("Dictionary Lookup", "dictionary computer"),
            ("System Command", "run command dir"),
        ]
        
        for test_name, command in utility_tests:
            self.test_function(test_name, command)
        
        # Advanced Integration Tests
        print("\n🔧 ADVANCED INTEGRATION TESTS")
        print("-" * 30)
        
        advanced_tests = [
            ("Complex YouTube Command", "open youtube and search for machine learning tutorials"),
            ("Complex Email Command", "email to manager about sick leave application"),
            ("Complex WhatsApp Command", "whatsapp message to john saying i will be late for meeting"),
            ("Complex Search Command", "search for best python libraries for ai development"),
            ("Complex System Command", "open calculator and take screenshot"),
        ]
        
        for test_name, command in advanced_tests:
            self.test_function(test_name, command)
        
        # Generate Test Report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ PASSED: {self.passed}")
        print(f"❌ FAILED: {self.failed}")
        print(f"📈 SUCCESS RATE: {success_rate:.1f}%")
        print(f"🔢 TOTAL TESTS: {total_tests}")
        
        # Bug Report
        if self.errors:
            print(f"\n🐛 BUG REPORT ({len(self.errors)} issues found)")
            print("-" * 40)
            
            for i, error in enumerate(self.errors, 1):
                print(f"\n{i}. {error['test']}")
                print(f"   Command: {error['command']}")
                print(f"   Error: {error['error']}")
                print(f"   Type: {type(error['error']).__name__}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 20)
        
        if success_rate >= 90:
            print("🎉 Excellent! JARVIS is working very well.")
        elif success_rate >= 75:
            print("👍 Good performance with minor issues to fix.")
        elif success_rate >= 50:
            print("⚠️  Moderate performance. Several bugs need attention.")
        else:
            print("🚨 Poor performance. Major debugging required.")
        
        # Critical Issues
        critical_keywords = ['chrome', 'driver', 'selenium', 'api', 'authentication']
        critical_errors = [e for e in self.errors if any(keyword in e['error'].lower() for keyword in critical_keywords)]
        
        if critical_errors:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical_errors)} found)")
            print("-" * 25)
            for error in critical_errors:
                print(f"• {error['test']}: {error['error']}")
        
        print(f"\n📝 DETAILED ERROR LOG")
        print("-" * 20)
        print("Check individual test outputs above for specific error details.")
        
        print(f"\n🔧 NEXT STEPS")
        print("-" * 12)
        print("1. Fix critical issues first (Chrome/API related)")
        print("2. Address failed tests one by one")
        print("3. Re-run test suite after fixes")
        print("4. Aim for 95%+ success rate")

def main():
    """Run complete JARVIS test suite"""
    
    print("🚀 Starting JARVIS Complete Project Test...")
    print("⚠️  Note: This will open applications and browsers during testing")
    
    # Confirmation
    confirm = input("\nProceed with testing? (y/n): ").lower()
    if confirm != 'y':
        print("Test cancelled.")
        return
    
    # Run tests
    test_suite = JarvisTestSuite()
    test_suite.run_complete_test_suite()
    
    print(f"\n🏁 Testing completed!")
    print("Check the report above for detailed results and bug analysis.")

if __name__ == "__main__":
    main()
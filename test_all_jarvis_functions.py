from jarvis import Jarvis

def test_all_jarvis_functions():
    """Test all JARVIS functions"""
    
    print("🤖 TESTING ALL JARVIS FUNCTIONS")
    print("=" * 50)
    
    bot = Jarvis()
    
    # Test categories with commands
    test_categories = {
        "🌐 Web & Search": [
            "open google",
            "search python programming",
            "youtube search music",
            "open amazon",
            "python wikipedia"
        ],
        "💻 System Control": [
            "open notepad",
            "close notepad", 
            "take screenshot",
            "cpu usage",
            "what is the time"
        ],
        "📧 Communication": [
            "open gmail",
            "compose email about meeting"
        ],
        "🎯 Information": [
            "tell me a joke",
            "weather report",
            "latest news"
        ],
        "🔧 System": [
            "open calculator",
            "open file explorer",
            "open settings"
        ],
        "🎤 Voice & AI": [
            "jarvis are you there",
            "who made you",
            "what does jarvis stand for"
        ]
    }
    
    total_tests = 0
    passed_tests = 0
    
    for category, commands in test_categories.items():
        print(f"\n{category}")
        print("-" * 30)
        
        for command in commands:
            total_tests += 1
            print(f"Testing: '{command}'")
            
            try:
                bot.execute_query(command)
                print("✅ PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"❌ FAILED: {e}")
            
            print()
    
    # Results summary
    print("=" * 50)
    print(f"📊 TEST RESULTS")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print("=" * 50)

if __name__ == "__main__":
    test_all_jarvis_functions()
from jarvis import Jarvis

def test_jarvis_wikipedia():
    """Test Wikipedia functionality in JARVIS"""
    
    print("Testing JARVIS Wikipedia Integration")
    print("=" * 40)
    
    # Initialize JARVIS
    bot = Jarvis()
    
    # Test Wikipedia commands
    test_commands = [
        "python wikipedia",
        "artificial intelligence wikipedia", 
        "wikipedia machine learning",
        "wikipedia java programming",
        "wikipedia"
    ]
    
    for command in test_commands:
        print(f"\nTesting command: '{command}'")
        try:
            bot.execute_query(command)
            print("✅ Command executed successfully")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 30)

if __name__ == "__main__":
    test_jarvis_wikipedia()
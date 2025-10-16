from jarvis import Jarvis
from amazon import open_amazon, search_amazon_product

def test_amazon_functions():
    """Test Amazon functions directly"""
    
    print("Testing Amazon Functions")
    print("=" * 40)
    
    # Test direct functions
    print("\n1. Testing open_amazon()")
    result = open_amazon()
    print(f"Result: {result}")
    
    print("\n2. Testing search_amazon_product()")
    result = search_amazon_product("laptop")
    print(f"Result: {result}")
    
    print("-" * 40)

def test_jarvis_amazon():
    """Test Amazon functionality in JARVIS"""
    
    print("Testing JARVIS Amazon Integration")
    print("=" * 40)
    
    bot = Jarvis()
    
    test_commands = [
        "open amazon",
        "amazon search laptop",
        "search amazon for books"
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
    test_amazon_functions()
    test_jarvis_amazon()
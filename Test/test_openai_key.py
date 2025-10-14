#!/usr/bin/env python3
"""Test OpenAI API key functionality"""

import os
from dotenv import load_dotenv
import openai

def test_openai_key():
    """Test if OpenAI API key is working"""
    
    print("=== OpenAI API Key Test ===\n")
    
    # Load environment variables
    load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
    
    # Check if key exists
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OPENAI_API_KEY found in .env file")
        return False
    
    if "your_ope" in api_key:
        print("❌ OpenAI API key is still placeholder")
        print("   Replace 'your_openai_api_key_here' with real key")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Set API key
    openai.api_key = api_key
    
    # Test API call
    try:
        print("\n🔄 Testing API connection...")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ],
            max_tokens=10,
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API Response: {result}")
        print("✅ OpenAI API key is working!")
        return True
        
    except openai.error.AuthenticationError:
        print("❌ Invalid API key - Authentication failed")
        return False
    except openai.error.RateLimitError:
        print("❌ Rate limit exceeded - Try again later")
        return False
    except openai.error.APIError as e:
        print(f"❌ API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_ai_intent():
    """Test AI intent recognition"""
    
    print("\n=== AI Intent Recognition Test ===")
    
    try:
        from ai_intent_recognition import get_ai_intent
        
        test_queries = [
            "open notepad",
            "search for python tutorials", 
            "play music on youtube"
        ]
        
        for query in test_queries:
            print(f"\nTesting: '{query}'")
            result = get_ai_intent(query)
            print(f"Intent: {result['intent']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Entities: {result['entities']}")
            
        print("\n✅ AI Intent Recognition working!")
        return True
        
    except Exception as e:
        print(f"❌ AI Intent Error: {e}")
        return False

if __name__ == "__main__":
    key_works = test_openai_key()
    
    if key_works:
        test_ai_intent()
    else:
        print("\n📝 To fix:")
        print("1. Get API key from: https://platform.openai.com/account/api-keys")
        print("2. Add to .env file: OPENAI_API_KEY=sk-your-actual-key")
        print("3. Run test again")
    
    print("\n=== Test completed ===")
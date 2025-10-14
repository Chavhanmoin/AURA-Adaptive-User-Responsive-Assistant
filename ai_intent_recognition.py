import openai
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"F:\J.A.R.V.I.S-master\.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Warning: OPENAI_API_KEY not found in .env file")

class AIIntentRecognizer:
    def __init__(self):
        self.system_prompt = """You are JARVIS AI assistant. Analyze user commands and return JSON with:
{
  "intent": "action_type",
  "entities": {"key": "value"},
  "confidence": 0.9,
  "action": "specific_action"
}

Analyze user commands and extract:
1. Primary intent (what user wants to do)
2. Target/object (what to act on) 
3. Additional parameters

Return flexible JSON that captures the user's true intention.
Examples:
- "open youtube and search car songs" → intent: search_youtube, entities: {query: "car songs"}
- "close notepad" → intent: close_app, entities: {app: "notepad"}
- "send message to john" → intent: send_message, entities: {contact: "john"}

Be flexible with entity names and capture the user's actual intent."""

    def recognize_intent(self, user_input):
        """Use OpenAI to recognize user intent"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze: '{user_input}'"}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            return json.loads(result)
            
        except Exception as e:
            print(f"AI Intent Recognition Error: {e}")
            # Fallback intent recognition for common patterns
            if "youtube" in user_input.lower() and "search" in user_input.lower():
                query = user_input.lower().replace("open", "").replace("youtube", "").replace("search", "").replace("and", "").strip()
                return {
                    "intent": "search_youtube",
                    "entities": {"query": query},
                    "confidence": 0.8,
                    "action": "youtube_search"
                }
            return {
                "intent": "other",
                "entities": {},
                "confidence": 0.1,
                "action": "fallback"
            }

def get_ai_intent(query):
    """Get AI-powered intent recognition"""
    recognizer = AIIntentRecognizer()
    return recognizer.recognize_intent(query)
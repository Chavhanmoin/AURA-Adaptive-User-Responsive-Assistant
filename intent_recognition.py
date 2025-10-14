import re
from difflib import get_close_matches

class IntentRecognizer:
    def __init__(self):
        self.intents = {
            'open_app': {
                'patterns': ['open', 'launch', 'start', 'run'],
                'entities': ['notepad', 'chrome', 'calculator', 'paint', 'code', 'spotify']
            },
            'close_app': {
                'patterns': ['close', 'exit', 'quit', 'stop'],
                'entities': ['notepad', 'chrome', 'calculator', 'paint', 'code', 'spotify']
            },
            'search_google': {
                'patterns': ['search', 'google', 'find', 'look up'],
                'keywords': ['search', 'google', 'find']
            },
            'search_youtube': {
                'patterns': ['youtube', 'video', 'watch'],
                'keywords': ['youtube', 'video', 'play']
            },
            'send_message': {
                'patterns': ['send', 'message', 'whatsapp', 'text'],
                'keywords': ['whatsapp', 'message', 'send']
            },
            'send_email': {
                'patterns': ['email', 'mail', 'compose'],
                'keywords': ['email', 'mail', 'gmail']
            },
            'system_info': {
                'patterns': ['cpu', 'battery', 'system', 'performance'],
                'keywords': ['cpu', 'battery', 'system']
            },
            'time_query': {
                'patterns': ['time', 'clock', 'what time'],
                'keywords': ['time', 'clock']
            },
            'weather_query': {
                'patterns': ['weather', 'temperature', 'forecast'],
                'keywords': ['weather', 'temperature']
            },
            'joke': {
                'patterns': ['joke', 'funny', 'laugh', 'humor'],
                'keywords': ['joke', 'funny']
            }
        }
    
    def extract_entities(self, text, intent):
        """Extract relevant entities from text"""
        entities = {}
        words = text.lower().split()
        
        if intent == 'open_app' or intent == 'close_app':
            for word in words:
                matches = get_close_matches(word, self.intents[intent]['entities'], n=1, cutoff=0.6)
                if matches:
                    entities['app'] = matches[0]
                    break
        
        elif intent in ['search_google', 'search_youtube']:
            # Extract search query
            for pattern in ['search for', 'search', 'find', 'look up', 'youtube']:
                if pattern in text.lower():
                    query = re.sub(rf'\b{pattern}\b', '', text.lower()).strip()
                    query = re.sub(r'\b(on|in|about|for)\b', '', query).strip()
                    if query:
                        entities['query'] = query
                        break
        
        return entities
    
    def recognize_intent(self, text):
        """Recognize user intent from text"""
        text_lower = text.lower()
        best_intent = None
        best_score = 0
        
        for intent, data in self.intents.items():
            score = 0
            
            # Check for pattern matches
            for pattern in data['patterns']:
                if pattern in text_lower:
                    score += 2
            
            # Check for keyword matches
            if 'keywords' in data:
                for keyword in data['keywords']:
                    if keyword in text_lower:
                        score += 1
            
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Extract entities for the recognized intent
        entities = {}
        if best_intent:
            entities = self.extract_entities(text, best_intent)
        
        return {
            'intent': best_intent,
            'confidence': best_score / 3,  # Normalize score
            'entities': entities,
            'original_text': text
        }

def process_user_intent(query):
    """Process user query and return structured intent"""
    recognizer = IntentRecognizer()
    return recognizer.recognize_intent(query)
"""
AI Response Module for AURA Assistant
Handles OpenAI API integration for conversational AI
"""

import openai
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIResponse:
    """Handles AI-powered responses using OpenAI API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Initialize OpenAI client"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.logger.warning("OpenAI API key not found in environment variables")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            self.logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI: {e}")
    
    def get_response(self, user_input, context=None):
        """Get AI response for user input"""
        try:
            if not self.client:
                return "AI service is not available right now."
            
            # Prepare system message
            system_message = """You are AURA, a helpful AI assistant integrated into a voice-controlled system. 
            You can help with questions, provide information, and assist with various tasks. 
            Keep responses concise and conversational since they will be spoken aloud.
            If asked about your capabilities, mention that you can control the computer, browse the web, 
            and manage smart home devices through voice commands."""
            
            messages = [
                {"role": "system", "content": system_message}
            ]
            
            # Add context if provided
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            # Add user message
            messages.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            self.logger.info(f"AI response generated for: {user_input[:50]}...")
            
            return ai_response
            
        except Exception as e:
            self.logger.error(f"AI response generation failed: {e}")
            return "I'm sorry, I'm having trouble processing that request right now."
    
    def generate_email_draft(self, recipient, subject, key_points):
        """Generate email draft using AI"""
        try:
            if not self.client:
                return "AI service is not available for email drafting."
            
            prompt = f"""
            Draft a professional email with the following details:
            Recipient: {recipient}
            Subject: {subject}
            Key points to include: {key_points}
            
            Make it concise and professional.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert email writer. Create professional, concise emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.5
            )
            
            email_draft = response.choices[0].message.content.strip()
            self.logger.info("Email draft generated successfully")
            
            return email_draft
            
        except Exception as e:
            self.logger.error(f"Email draft generation failed: {e}")
            return "Failed to generate email draft."
    
    def summarize_text(self, text, max_length=100):
        """Summarize given text"""
        try:
            if not self.client:
                return "AI service is not available for summarization."
            
            prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length + 50,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            self.logger.info("Text summarized successfully")
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Text summarization failed: {e}")
            return "Failed to summarize text."
    
    def answer_question(self, question, context=None):
        """Answer specific questions with optional context"""
        try:
            if not self.client:
                return "AI service is not available right now."
            
            messages = [
                {"role": "system", "content": "You are a knowledgeable assistant. Provide accurate, helpful answers."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Additional context: {context}"})
            
            messages.append({"role": "user", "content": question})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200,
                temperature=0.5
            )
            
            answer = response.choices[0].message.content.strip()
            self.logger.info(f"Question answered: {question[:50]}...")
            
            return answer
            
        except Exception as e:
            self.logger.error(f"Question answering failed: {e}")
            return "I'm sorry, I couldn't find an answer to that question."
    
    def generate_code_explanation(self, code):
        """Explain code functionality"""
        try:
            if not self.client:
                return "AI service is not available for code explanation."
            
            prompt = f"Explain what this code does in simple terms:\n\n{code}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a programming expert. Explain code clearly and simply."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.3
            )
            
            explanation = response.choices[0].message.content.strip()
            self.logger.info("Code explanation generated")
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Code explanation failed: {e}")
            return "Failed to explain the code."
    
    def get_weather_info(self, location):
        """Get weather information (placeholder - would need weather API)"""
        try:
            # This is a placeholder - in a real implementation, you'd integrate with a weather API
            prompt = f"Provide general weather advice for someone in {location}. Mention that for real-time weather, they should check a weather app or website."
            
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Provide helpful weather-related advice."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.5
                )
                
                return response.choices[0].message.content.strip()
            else:
                return f"For current weather in {location}, please check a weather app or website."
                
        except Exception as e:
            self.logger.error(f"Weather info request failed: {e}")
            return "I can't get weather information right now. Please check a weather app."
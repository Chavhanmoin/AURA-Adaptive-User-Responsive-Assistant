"""
Command Handler Module for AURA Assistant
Routes commands to appropriate modules based on intent
"""

import re
import logging
from modules.system_control import SystemControl
from modules.web_automation import WebAutomation
from modules.sinric_control import SinricControl
from modules.ai_response import AIResponse

class CommandHandler:
    """Handles command routing and intent recognition"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_control = SystemControl()
        self.web_automation = WebAutomation()
        self.sinric_control = SinricControl()
        self.ai_response = AIResponse()
        
        # Command patterns
        self.patterns = {
            'system': [
                r'open\s+(\w+)',
                r'close\s+(\w+)',
                r'shutdown|shut down',
                r'restart|reboot',
                r'volume\s+(up|down|\d+)',
                r'brightness\s+(up|down|\d+)',
                r'sleep|hibernate'
            ],
            'web': [
                r'search\s+(.+)',
                r'google\s+(.+)',
                r'youtube\s+(.+)',
                r'play\s+(.+)',
                r'email\s+(.+)',
                r'whatsapp\s+(.+)',
                r'open\s+(website|site)\s+(.+)'
            ],
            'iot': [
                r'turn\s+(on|off)\s+(.+)',
                r'set\s+(.+)\s+to\s+(\d+)',
                r'dim\s+(.+)',
                r'brighten\s+(.+)',
                r'(lights?|fan|ac|tv)\s+(on|off)'
            ],
            'ai': [
                r'what\s+is\s+(.+)',
                r'tell\s+me\s+about\s+(.+)',
                r'explain\s+(.+)',
                r'help\s+(.+)',
                r'how\s+to\s+(.+)'
            ]
        }
    
    def handle_command(self, command):
        """Route command to appropriate handler"""
        try:
            command = command.lower().strip()
            self.logger.info(f"Processing command: {command}")
            
            # Check for system commands
            if self.match_pattern(command, 'system'):
                return self.handle_system_command(command)
            
            # Check for web commands
            elif self.match_pattern(command, 'web'):
                return self.handle_web_command(command)
            
            # Check for IoT commands
            elif self.match_pattern(command, 'iot'):
                return self.handle_iot_command(command)
            
            # Default to AI response
            else:
                return self.handle_ai_command(command)
                
        except Exception as e:
            self.logger.error(f"Command handling error: {e}")
            return "Sorry, I encountered an error processing that command."
    
    def match_pattern(self, command, category):
        """Check if command matches any pattern in category"""
        for pattern in self.patterns[category]:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False
    
    def handle_system_command(self, command):
        """Handle system control commands"""
        try:
            # Open application
            if 'open' in command:
                app_match = re.search(r'open\s+(\w+)', command)
                if app_match:
                    app_name = app_match.group(1)
                    success = self.system_control.open_application(app_name)
                    return f"Opening {app_name}" if success else f"Could not open {app_name}"
            
            # Close application
            elif 'close' in command:
                app_match = re.search(r'close\s+(\w+)', command)
                if app_match:
                    app_name = app_match.group(1)
                    success = self.system_control.close_application(app_name)
                    return f"Closing {app_name}" if success else f"Could not close {app_name}"
            
            # System operations
            elif 'shutdown' in command or 'shut down' in command:
                self.system_control.shutdown()
                return "Shutting down the system"
            
            elif 'restart' in command or 'reboot' in command:
                self.system_control.restart()
                return "Restarting the system"
            
            # Volume control
            elif 'volume' in command:
                vol_match = re.search(r'volume\s+(up|down|\d+)', command)
                if vol_match:
                    action = vol_match.group(1)
                    if action == 'up':
                        self.system_control.volume_up()
                        return "Volume increased"
                    elif action == 'down':
                        self.system_control.volume_down()
                        return "Volume decreased"
                    else:
                        level = int(action)
                        self.system_control.set_volume(level)
                        return f"Volume set to {level}%"
            
            # Brightness control
            elif 'brightness' in command:
                bright_match = re.search(r'brightness\s+(up|down|\d+)', command)
                if bright_match:
                    action = bright_match.group(1)
                    if action == 'up':
                        self.system_control.brightness_up()
                        return "Brightness increased"
                    elif action == 'down':
                        self.system_control.brightness_down()
                        return "Brightness decreased"
                    else:
                        level = int(action)
                        self.system_control.set_brightness(level)
                        return f"Brightness set to {level}%"
            
            return "System command executed"
            
        except Exception as e:
            self.logger.error(f"System command error: {e}")
            return "Error executing system command"
    
    def handle_web_command(self, command):
        """Handle web automation commands"""
        try:
            # Search commands
            if 'search' in command or 'google' in command:
                search_match = re.search(r'(?:search|google)\s+(.+)', command)
                if search_match:
                    query = search_match.group(1)
                    self.web_automation.google_search(query)
                    return f"Searching for {query}"
            
            # YouTube commands
            elif 'youtube' in command or 'play' in command:
                video_match = re.search(r'(?:youtube|play)\s+(.+)', command)
                if video_match:
                    query = video_match.group(1)
                    self.web_automation.youtube_search(query)
                    return f"Playing {query} on YouTube"
            
            # Email commands
            elif 'email' in command:
                email_match = re.search(r'email\s+(.+)', command)
                if email_match:
                    content = email_match.group(1)
                    self.web_automation.compose_email(content)
                    return "Composing email"
            
            # WhatsApp commands
            elif 'whatsapp' in command:
                msg_match = re.search(r'whatsapp\s+(.+)', command)
                if msg_match:
                    message = msg_match.group(1)
                    self.web_automation.send_whatsapp(message)
                    return "Sending WhatsApp message"
            
            return "Web command executed"
            
        except Exception as e:
            self.logger.error(f"Web command error: {e}")
            return "Error executing web command"
    
    def handle_iot_command(self, command):
        """Handle IoT device commands"""
        try:
            # Turn on/off devices
            if 'turn' in command:
                turn_match = re.search(r'turn\s+(on|off)\s+(.+)', command)
                if turn_match:
                    action = turn_match.group(1)
                    device = turn_match.group(2)
                    success = self.sinric_control.control_device(device, action)
                    return f"Turning {action} {device}" if success else f"Could not control {device}"
            
            # Set device values
            elif 'set' in command:
                set_match = re.search(r'set\s+(.+)\s+to\s+(\d+)', command)
                if set_match:
                    device = set_match.group(1)
                    value = int(set_match.group(2))
                    success = self.sinric_control.set_device_value(device, value)
                    return f"Setting {device} to {value}" if success else f"Could not set {device}"
            
            return "IoT command executed"
            
        except Exception as e:
            self.logger.error(f"IoT command error: {e}")
            return "Error executing IoT command"
    
    def handle_ai_command(self, command):
        """Handle AI/conversational commands"""
        try:
            response = self.ai_response.get_response(command)
            return response
            
        except Exception as e:
            self.logger.error(f"AI command error: {e}")
            return "I'm sorry, I couldn't process that request right now."
"""
System Control Module for AURA Assistant
Handles PC automation, app control, and system operations
"""

import os
import subprocess
import pyautogui
import psutil
import logging
from pathlib import Path

class SystemControl:
    """Handles system-level operations and app control"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common application paths
        self.app_paths = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'vscode': r'C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE'
        }
    
    def open_application(self, app_name):
        """Open an application by name"""
        try:
            app_name = app_name.lower()
            
            if app_name in self.app_paths:
                app_path = self.app_paths[app_name]
                
                # Handle user-specific paths
                if '{}' in app_path:
                    username = os.getenv('USERNAME')
                    app_path = app_path.format(username)
                
                # Check if file exists
                if os.path.exists(app_path):
                    subprocess.Popen([app_path])
                    self.logger.info(f"Opened {app_name}")
                    return True
                else:
                    # Try to open using system command
                    os.system(f'start {app_name}')
                    return True
            else:
                # Try generic approach
                os.system(f'start {app_name}')
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to open {app_name}: {e}")
            return False
    
    def close_application(self, app_name):
        """Close an application by name"""
        try:
            app_name = app_name.lower()
            
            # Map common names to process names
            process_names = {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'vscode': 'Code.exe',
                'word': 'WINWORD.EXE',
                'excel': 'EXCEL.EXE',
                'powerpoint': 'POWERPNT.EXE'
            }
            
            process_name = process_names.get(app_name, f'{app_name}.exe')
            
            # Find and terminate process
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    proc.terminate()
                    self.logger.info(f"Closed {app_name}")
                    return True
            
            self.logger.warning(f"Process {app_name} not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to close {app_name}: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the system"""
        try:
            os.system('shutdown /s /t 1')
            self.logger.info("System shutdown initiated")
            
        except Exception as e:
            self.logger.error(f"Failed to shutdown: {e}")
    
    def restart(self):
        """Restart the system"""
        try:
            os.system('shutdown /r /t 1')
            self.logger.info("System restart initiated")
            
        except Exception as e:
            self.logger.error(f"Failed to restart: {e}")
    
    def volume_up(self):
        """Increase system volume"""
        try:
            pyautogui.press('volumeup')
            self.logger.info("Volume increased")
            
        except Exception as e:
            self.logger.error(f"Failed to increase volume: {e}")
    
    def volume_down(self):
        """Decrease system volume"""
        try:
            pyautogui.press('volumedown')
            self.logger.info("Volume decreased")
            
        except Exception as e:
            self.logger.error(f"Failed to decrease volume: {e}")
    
    def set_volume(self, level):
        """Set volume to specific level (0-100)"""
        try:
            # Mute first, then set volume
            pyautogui.press('volumemute')
            pyautogui.press('volumemute')  # Unmute
            
            # Press volume down to minimum
            for _ in range(50):
                pyautogui.press('volumedown')
            
            # Press volume up to desired level
            steps = int(level / 2)  # Approximate steps
            for _ in range(steps):
                pyautogui.press('volumeup')
                
            self.logger.info(f"Volume set to {level}%")
            
        except Exception as e:
            self.logger.error(f"Failed to set volume: {e}")
    
    def brightness_up(self):
        """Increase screen brightness"""
        try:
            # Use Windows key + A to open action center, then use arrow keys
            pyautogui.hotkey('win', 'a')
            pyautogui.sleep(0.5)
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('escape')
            self.logger.info("Brightness increased")
            
        except Exception as e:
            self.logger.error(f"Failed to increase brightness: {e}")
    
    def brightness_down(self):
        """Decrease screen brightness"""
        try:
            pyautogui.hotkey('win', 'a')
            pyautogui.sleep(0.5)
            pyautogui.press('tab')
            pyautogui.press('left')
            pyautogui.press('escape')
            self.logger.info("Brightness decreased")
            
        except Exception as e:
            self.logger.error(f"Failed to decrease brightness: {e}")
    
    def set_brightness(self, level):
        """Set brightness to specific level (0-100)"""
        try:
            # This is a simplified approach - actual implementation may vary
            # depending on the system and drivers
            steps = int(level / 10)
            
            pyautogui.hotkey('win', 'a')
            pyautogui.sleep(0.5)
            pyautogui.press('tab')
            
            # Reset to minimum
            for _ in range(10):
                pyautogui.press('left')
            
            # Set to desired level
            for _ in range(steps):
                pyautogui.press('right')
                
            pyautogui.press('escape')
            self.logger.info(f"Brightness set to {level}%")
            
        except Exception as e:
            self.logger.error(f"Failed to set brightness: {e}")
    
    def sleep_system(self):
        """Put system to sleep"""
        try:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            self.logger.info("System put to sleep")
            
        except Exception as e:
            self.logger.error(f"Failed to sleep system: {e}")
    
    def lock_screen(self):
        """Lock the screen"""
        try:
            pyautogui.hotkey('win', 'l')
            self.logger.info("Screen locked")
            
        except Exception as e:
            self.logger.error(f"Failed to lock screen: {e}")
    
    def take_screenshot(self, filename=None):
        """Take a screenshot"""
        try:
            if not filename:
                filename = f"screenshot_{int(time.time())}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            self.logger.info(f"Screenshot saved as {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return None
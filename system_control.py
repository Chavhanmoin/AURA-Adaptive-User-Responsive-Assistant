import os
import subprocess
import psutil
import winreg
from pathlib import Path

class SystemController:
    def __init__(self):
        self.installed_apps = self._get_installed_apps()
    
    def _get_installed_apps(self):
        """Get list of installed applications from registry"""
        apps = {}
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                    apps[name.lower()] = path
                except:
                    pass
        except:
            pass
        return apps
    
    def open_application(self, app_name):
        """Open any application by name"""
        app_name = app_name.lower()
        
        # Direct command mapping for common apps
        app_commands = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'calc': 'calc.exe',
            'paint': 'mspaint.exe',
            'mspaint': 'mspaint.exe',
            'chrome': r'"C:\Program Files\Google\Chrome\Application\chrome.exe"',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe'
        }
        
        # Skip VS Code - prioritize folder shortcuts
        if app_name in ['documents', 'desktop', 'downloads', 'pictures', 'music']:
            return self.open_file_or_folder(app_name)
        
        if app_name in app_commands:
            try:
                subprocess.Popen(app_commands[app_name], shell=True)
                return f"Opened {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {e}"
        
        # Try direct command
        try:
            subprocess.Popen(app_name, shell=True)
            return f"Opened {app_name}"
        except:
            pass
        
        # Try with .exe extension
        try:
            subprocess.Popen(f"{app_name}.exe", shell=True)
            return f"Opened {app_name}.exe"
        except:
            pass
        
        return f"Could not find application: {app_name}"
    
    def close_application(self, app_name):
        """Close any running application with exact matching"""
        # Exact process name mapping only
        process_map = {
            'notepad': 'notepad.exe',
            'calculator': 'CalculatorApp.exe',
            'calc': 'CalculatorApp.exe', 
            'paint': 'mspaint.exe',
            'mspaint': 'mspaint.exe',
            'paints': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'spotify': 'Spotify.exe'
        }
        
        print(f"DEBUG: Trying to close '{app_name}'")
        
        # Only use exact matches from the map
        if app_name.lower() not in process_map:
            return f"App '{app_name}' not in safe close list. Use exact process name."
        
        target_process = process_map[app_name.lower()]
        print(f"DEBUG: Looking for process '{target_process}'")
        
        killed = []
        running_processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                running_processes.append(proc.info['name'])
                # Only exact match
                if proc.info['name'].lower() == target_process.lower():
                    print(f"DEBUG: Found and killing process {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    killed.append(proc.info['name'])
            except Exception as e:
                print(f"DEBUG: Error with process: {e}")
        
        print(f"DEBUG: Running processes containing 'notepad': {[p for p in running_processes if 'notepad' in p.lower()]}")
        
        if killed:
            return f"Closed: {', '.join(killed)}"
        return f"No running process found for: {app_name}. Target was: {target_process}"
    
    def open_file_or_folder(self, path):
        """Open any file or folder"""
        try:
            # Common folder shortcuts
            shortcuts = {
                'documents': os.path.expanduser('~\\Documents'),
                'desktop': os.path.expanduser('~\\Desktop'),
                'downloads': os.path.expanduser('~\\Downloads'),
                'pictures': os.path.expanduser('~\\Pictures'),
                'music': os.path.expanduser('~\\Music')
            }
            
            # Check shortcuts first
            if path.lower() in shortcuts:
                os.startfile(shortcuts[path.lower()])
                return f"Opened: {shortcuts[path.lower()]}"
            
            if os.path.exists(path):
                os.startfile(path)
                return f"Opened: {path}"
            
            # Try expanding user path
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                os.startfile(expanded_path)
                return f"Opened: {expanded_path}"
            
            return f"File/folder not found: {path}"
        except Exception as e:
            return f"Error opening {path}: {str(e)}"
    
    def system_command(self, command):
        """Execute any system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return f"Command executed: {command}\nOutput: {result.stdout}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

# Integration functions for jarvis.py
def open_anything(name):
    """Universal open function"""
    controller = SystemController()
    
    # Check if it's a common folder first
    folders = ['documents', 'desktop', 'downloads', 'pictures', 'music']
    if name.lower() in folders:
        return controller.open_file_or_folder(name)
    
    # Try as application
    result = controller.open_application(name)
    if "Could not find" not in result:
        return result
    
    # Try as file/folder
    return controller.open_file_or_folder(name)

def close_anything(name):
    """Universal close function"""
    controller = SystemController()
    return controller.close_application(name)

def execute_system_command(command):
    """Execute system command"""
    controller = SystemController()
    return controller.system_command(command)
import os
import shutil
import subprocess
from pathlib import Path
from helpers import speak

def create_file(file_path, content=""):
    """Create a new file"""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            f.write(content)
        
        speak(f"File created: {path.name}")
        return f"File created successfully: {file_path}"
    except Exception as e:
        speak("Failed to create file")
        return f"Error: {str(e)}"

def create_folder(folder_path):
    """Create a new folder"""
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        speak(f"Folder created: {Path(folder_path).name}")
        return f"Folder created successfully: {folder_path}"
    except Exception as e:
        speak("Failed to create folder")
        return f"Error: {str(e)}"

def open_file(file_path):
    """Open a file with default application"""
    try:
        if os.path.exists(file_path):
            os.startfile(file_path)
            speak(f"Opening {Path(file_path).name}")
            return f"File opened: {file_path}"
        else:
            speak("File not found")
            return f"File not found: {file_path}"
    except Exception as e:
        speak("Failed to open file")
        return f"Error: {str(e)}"

def open_folder(folder_path):
    """Open a folder in file explorer"""
    try:
        if os.path.exists(folder_path):
            subprocess.run(['explorer', folder_path])
            speak(f"Opening {Path(folder_path).name} folder")
            return f"Folder opened: {folder_path}"
        else:
            speak("Folder not found")
            return f"Folder not found: {folder_path}"
    except Exception as e:
        speak("Failed to open folder")
        return f"Error: {str(e)}"

def delete_file(file_path):
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            speak(f"File deleted: {Path(file_path).name}")
            return f"File deleted: {file_path}"
        else:
            speak("File not found")
            return f"File not found: {file_path}"
    except Exception as e:
        speak("Failed to delete file")
        return f"Error: {str(e)}"

def delete_folder(folder_path):
    """Delete a folder"""
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            speak(f"Folder deleted: {Path(folder_path).name}")
            return f"Folder deleted: {folder_path}"
        else:
            speak("Folder not found")
            return f"Folder not found: {folder_path}"
    except Exception as e:
        speak("Failed to delete folder")
        return f"Error: {str(e)}"

def copy_file(source, destination):
    """Copy a file"""
    try:
        shutil.copy2(source, destination)
        speak(f"File copied to {Path(destination).name}")
        return f"File copied from {source} to {destination}"
    except Exception as e:
        speak("Failed to copy file")
        return f"Error: {str(e)}"

def move_file(source, destination):
    """Move a file"""
    try:
        shutil.move(source, destination)
        speak(f"File moved to {Path(destination).name}")
        return f"File moved from {source} to {destination}"
    except Exception as e:
        speak("Failed to move file")
        return f"Error: {str(e)}"

def list_files(folder_path):
    """List files in a folder"""
    try:
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            speak(f"Found {len(files)} items in folder")
            return f"Files in {folder_path}: {files}"
        else:
            speak("Folder not found")
            return f"Folder not found: {folder_path}"
    except Exception as e:
        speak("Failed to list files")
        return f"Error: {str(e)}"
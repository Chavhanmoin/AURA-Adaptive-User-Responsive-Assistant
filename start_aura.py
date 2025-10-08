#!/usr/bin/env python3
"""
AURA Assistant Startup Script
Simple launcher with error handling
"""

import sys
import os
import logging
from pathlib import Path

def setup_environment():
    """Setup environment and check dependencies"""
    try:
        # Create required directories
        directories = [
            'data/logs',
            'assets/sounds',
            'assets/images'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Check if .env file exists
        if not Path('.env').exists():
            print("Warning: .env file not found. Please copy .env.example to .env and configure your API keys.")
            return False
        
        return True
        
    except Exception as e:
        print(f"Environment setup failed: {e}")
        return False

def main():
    """Main startup function"""
    print("Starting AURA Assistant...")
    
    if not setup_environment():
        print("Environment setup failed. Please check the configuration.")
        return
    
    try:
        from main import main as aura_main
        aura_main()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install required dependencies: pip install -r requirements.txt")
        
    except KeyboardInterrupt:
        print("\nAURA Assistant stopped by user")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.exception("Startup error")

if __name__ == "__main__":
    main()
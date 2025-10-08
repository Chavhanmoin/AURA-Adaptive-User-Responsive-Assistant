# Hybrid A.U.R.A Assistant

AI + Automation + IoT Voice-Controlled Assistant

## Features

- **Voice Control**: Wake word detection with "Hey Aura"
- **System Automation**: Control PC applications, volume, brightness
- **Web Automation**: Google search, YouTube, Gmail, WhatsApp Web
- **AI Integration**: OpenAI-powered conversational responses
- **IoT Control**: Smart home devices via Sinric Pro
- **Task Scheduling**: Automated tasks and reminders

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

3. **Run AURA**
   ```bash
   python start_aura.py
   ```

## Configuration

### Required API Keys

- **OpenAI API Key**: For AI responses
- **Sinric Pro**: For IoT device control
- **Picovoice Access Key**: For wake word detection

### Environment Variables (.env)

```env
OPENAI_API_KEY=your_key_here
SINRIC_APP_KEY=your_key_here
SINRIC_APP_SECRET=your_secret_here
PICOVOICE_ACCESS_KEY=your_key_here
```

## Voice Commands

### System Control
- "Open Chrome/Notepad/Calculator"
- "Close Chrome"
- "Shutdown/Restart"
- "Volume up/down"
- "Set volume to 50"
- "Brightness up/down"

### Web Automation
- "Search for Python tutorials"
- "Play music on YouTube"
- "Open Gmail"
- "Send WhatsApp message"

### IoT Control
- "Turn on living room light"
- "Set brightness to 70"
- "Turn off all lights"

### AI Queries
- "What is machine learning?"
- "Tell me about the weather"
- "Help me with coding"

## Project Structure

```
AURA/
├── main.py                 # Main entry point
├── start_aura.py          # Startup script
├── requirements.txt       # Dependencies
├── modules/
│   ├── speech_engine.py   # Voice recognition & TTS
│   ├── command_handler.py # Command routing
│   ├── system_control.py  # PC automation
│   ├── web_automation.py  # Browser automation
│   ├── ai_response.py     # OpenAI integration
│   ├── sinric_control.py  # IoT control
│   └── scheduler.py       # Task scheduling
├── data/
│   ├── user_data.json     # User preferences
│   └── logs/              # Application logs
└── assets/
    ├── sounds/            # Audio files
    └── images/            # Image assets
```

## Troubleshooting

### Common Issues

1. **Microphone not working**: Check Windows microphone permissions
2. **Wake word not detected**: Verify Picovoice API key
3. **Web automation fails**: Update Chrome and webdriver
4. **IoT devices not responding**: Check Sinric Pro configuration

### Dependencies Issues

If you encounter package installation issues:

```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages individually if needed
pip install SpeechRecognition pyttsx3 selenium openai
```

## Building Executable

To create a standalone .exe file:

```bash
pyinstaller --onefile --windowed main.py
```

## License

This project is for educational and personal use.
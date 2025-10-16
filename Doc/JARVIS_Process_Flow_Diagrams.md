# J.A.R.V.I.S Process Flow Diagrams

## 1. Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        J.A.R.V.I.S SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   INPUT     │    │ PROCESSING  │    │   OUTPUT    │        │
│  │             │    │             │    │             │        │
│  │ 🎤 Voice    │───▶│ 🧠 AI       │───▶│ 🔊 Speech   │        │
│  │ ⌨️  Keyboard │    │ 🔍 Intent   │    │ 💻 Actions  │        │
│  │ 👁️  Camera   │    │ 📋 Rules    │    │ 🌐 Web      │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Main Process Flow

```
START
  │
  ▼
┌─────────────────┐
│ System Init     │
│ • Load .env     │
│ • Setup TTS     │
│ • Chrome config │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ Greeting        │
│ • Good Morning  │
│ • CPU Status    │
│ • Weather Info  │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ Activation Mode │
│ • Wake Word     │
│ • Ctrl+K        │
│ • Direct Voice  │
└─────────────────┘
  │
  ▼
┌─────────────────┐    ┌─────────────────┐
│ Listen for      │───▶│ Voice Capture   │
│ "Jarvis" or     │    │ • Microphone    │
│ Keyboard Input  │    │ • Google API    │
└─────────────────┘    │ • 5s timeout    │
  ▲                    └─────────────────┘
  │                              │
  │                              ▼
  │                    ┌─────────────────┐
  │                    │ Intent Analysis │
  │                    │ • AI (OpenAI)   │
  │                    │ • Rules         │
  │                    │ • Direct Match  │
  │                    └─────────────────┘
  │                              │
  │                              ▼
  │                    ┌─────────────────┐
  │                    │ Command Execute │
  │                    │ • System Ctrl   │
  │                    │ • Web Auto      │
  │                    │ • Info Service  │
  │                    └─────────────────┘
  │                              │
  │                              ▼
  │                    ┌─────────────────┐
  │                    │ Response        │
  │                    │ • TTS Output    │
  │                    │ • Action Result │
  │                    │ • Error Handle  │
  │                    └─────────────────┘
  │                              │
  └──────────────────────────────┘
```

## 3. Intent Recognition Pipeline

```
User Command: "Open YouTube and search car songs"
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: AI INTENT                      │
├─────────────────────────────────────────────────────────────┤
│ OpenAI GPT-3.5 Analysis                                    │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│ │   Intent    │  │  Entities   │  │ Confidence  │        │
│ │search_youtube│  │query:"car   │  │    0.95     │        │
│ │             │  │songs"       │  │             │        │
│ └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
     │ (if confidence > 0.5)
     ▼
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 2: RULE-BASED                      │
├─────────────────────────────────────────────────────────────┤
│ Pattern Matching                                           │
│ • "youtube" + "search" → youtube_search()                  │
│ • "open" + app_name → open_app()                          │
│ • "close" + app_name → close_app()                        │
└─────────────────────────────────────────────────────────────┘
     │ (if no AI match)
     ▼
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 3: DIRECT MATCH                     │
├─────────────────────────────────────────────────────────────┤
│ Simple String Matching                                     │
│ • if 'youtube' in query and 'search' in query             │
│ • elif 'time' in query                                     │
│ • elif 'weather' in query                                  │
└─────────────────────────────────────────────────────────────┘
```

## 4. Command Execution Flow

```
┌─────────────────┐
│ Command Router  │
└─────────────────┘
         │
    ┌────┴────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼
┌─────────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ System  │ │ Web  │ │ Info │ │ Comm │ │ AI   │
│ Control │ │ Auto │ │ Serv │ │      │ │ Proc │
└─────────┘ └──────┘ └──────┘ └──────┘ └──────┘
     │         │        │        │        │
     ▼         ▼        ▼        ▼        ▼
┌─────────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│• Open   │ │• Google│ │• Weather│ │• Email│ │• GPT │
│• Close  │ │• YouTube│ │• CPU   │ │• WhatsApp│ │• NLP │
│• Files  │ │• WhatsApp│ │• Time │ │• SMS  │ │• Context│
│• Apps   │ │• Gmail │ │• Jokes │ │      │ │      │
└─────────┘ └──────┘ └──────┘ └──────┘ └──────┘
```

## 5. Voice Recognition Process

```
┌─────────────────────────────────────────────────────────────┐
│                  VOICE RECOGNITION FLOW                     │
└─────────────────────────────────────────────────────────────┘

🎤 Microphone Input
     │
     ▼ (0.3s)
┌─────────────────┐
│ Ambient Noise   │
│ Calibration     │
└─────────────────┘
     │
     ▼ (5s timeout)
┌─────────────────┐
│ Active Listening│
│ • Phrase limit  │
│ • 15 seconds    │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Google Speech   │
│ Recognition API │
│ • English-India │
└─────────────────┘
     │
     ▼
┌─────────────────┐    ┌─────────────────┐
│ Text Output     │───▶│ Command Process │
│ • Lowercase     │    │ • Intent Recog  │
│ • Trimmed       │    │ • Execution     │
└─────────────────┘    └─────────────────┘
     │
     ▼ (if failed)
┌─────────────────┐
│ Return 'None'   │
│ • Retry Loop    │
│ • Error Handle  │
└─────────────────┘
```

## 6. Web Automation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WEB AUTOMATION SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Chrome    │    │  Selenium   │    │   Target    │    │
│  │   Driver    │───▶│  WebDriver  │───▶│  Websites   │    │
│  │             │    │             │    │             │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │• Profile    │    │• Element    │    │• Google     │    │
│  │• Options    │    │  Location   │    │• YouTube    │    │
│  │• Anti-detect│    │• Click/Type │    │• WhatsApp   │    │
│  │• Headless   │    │• Wait/Retry │    │• Gmail      │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 7. Error Handling & Recovery

```
┌─────────────────┐
│ Command Execute │
└─────────────────┘
         │
         ▼
    ┌─────────┐
    │ Success?│
    └─────────┘
    │         │
   Yes        No
    │         │
    ▼         ▼
┌─────────┐ ┌─────────────────┐
│Response │ │ Error Analysis  │
│& TTS    │ └─────────────────┘
└─────────┘          │
    │                ▼
    │         ┌─────────────────┐
    │         │ Error Type?     │
    │         └─────────────────┘
    │         │      │      │
    │      Speech  API   System
    │         │      │      │
    │         ▼      ▼      ▼
    │    ┌────────┐ ┌────┐ ┌────┐
    │    │ Retry  │ │Fall│ │Log │
    │    │ Voice  │ │back│ │&   │
    │    │ Input  │ │Mode│ │Msg │
    │    └────────┘ └────┘ └────┘
    │         │      │      │
    └─────────┴──────┴──────┘
```

## 8. Module Interaction Diagram

```
                    jarvis.py (Main Controller)
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ helpers.py  │    │system_ctrl  │    │web_automation│
│             │    │             │    │             │
│• takeCommand│    │• open_app   │    │• google_srch│
│• speak      │    │• close_app  │    │• youtube    │
│• weather    │    │• file_ops   │    │• whatsapp   │
│• cpu        │    │• sys_cmd    │    │• gmail      │
│• screenshot │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ai_intent.py │    │intent_recog │    │gmail_service│
│             │    │             │    │             │
│• OpenAI API │    │• patterns   │    │• API calls  │
│• GPT-3.5    │    │• rules      │    │• OAuth      │
│• NLP        │    │• fallback   │    │• compose    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 9. Data Flow Diagram

```
User Voice Input
       │
       ▼
┌─────────────┐
│ Speech API  │ ──── Internet Required
└─────────────┘
       │
       ▼
┌─────────────┐
│ Text String │
└─────────────┘
       │
       ▼
┌─────────────┐
│ AI Analysis │ ──── OpenAI API (Internet)
└─────────────┘
       │
       ▼
┌─────────────┐
│ Intent JSON │
│ {           │
│  intent: "" │
│  entities:{}│
│  confidence │
│ }           │
└─────────────┘
       │
       ▼
┌─────────────┐
│ Command     │
│ Execution   │
└─────────────┘
       │
    ┌──┴──┬──────┬──────┐
    ▼     ▼      ▼      ▼
┌──────┐┌────┐┌────┐┌────┐
│System││Web ││Info││Comm│
│ Ops  ││Auto││Serv││    │
└──────┘└────┘└────┘└────┘
    │     │      │      │
    └──┬──┴──────┴──────┘
       ▼
┌─────────────┐
│ TTS Output  │
│ + Actions   │
└─────────────┘
```

## 10. Session Lifecycle

```
Application Start
       │
       ▼
┌─────────────┐
│ Initialize  │
│ • Load env  │
│ • Setup TTS │
│ • Chrome    │
└─────────────┘
       │
       ▼
┌─────────────┐
│ Greeting    │
│ • Time-based│
│ • Status    │
└─────────────┘
       │
       ▼
┌─────────────┐ ◄──────────────┐
│ Listen Loop │                │
│ • Wake word │                │
│ • Ctrl+K    │                │
└─────────────┘                │
       │                       │
       ▼                       │
┌─────────────┐                │
│ Process Cmd │                │
│ • Recognize │                │
│ • Execute   │                │
│ • Respond   │                │
└─────────────┘                │
       │                       │
       ▼                       │
┌─────────────┐                │
│ Continue?   │ ──Yes──────────┘
└─────────────┘
       │ No
       ▼
┌─────────────┐
│ Shutdown    │
│ • Cleanup   │
│ • Goodbye   │
│ • Exit      │
└─────────────┘
```

This comprehensive set of diagrams shows the complete J.A.R.V.I.S system architecture and process flows from initialization to shutdown.
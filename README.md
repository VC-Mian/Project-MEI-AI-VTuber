# Project_MEI

This is MEi an AI VTuber that interacts with Twitch viewers in real-time. 
Inspired by Vedal who programed the AI Vtuber on Twutch, Neruo-sama, this project demonstrates the integration of large language models, real-time chat processing, 
and character animation to create an engaging streaming experience. 

## Features
1. Real-time AI responses using Claude API
2. Custom personality
3. Twitch chat integration with message queue system
4. Automated lip-sync animation via VTube Studio API
5. Text-to-speech voice synthesis
6. Auto-reconnection handling for stable streaming

## Tech Stack
**Core Technologies**
- Language: Python 3.x
- AI/ML: Claude API (Anthropic Sonnet 4)
- Framework: asyncio for asynchronous processing

**APIs & Libraries**

- TwitchIO 2.9.1 - Twitch chat integration
- pyvts - VTube Studio WebSocket API
- pyttsx3 - Text-to-speech engine
- python-dotenv - Environment configuration

**Tools & Platforms**

- VTube Studio
- Live2D character rendering
- OBS Studio - Stream broadcasting (Optional)
- Git
- Version control

## Running it
**Prerequisites**

- Python 3.8 or higher
- VTube Studio
- OBS Studio (optional, for streaming)
- Twitch account
- Claude API key (or OpenAI API key)

Clone the repository

```bash
   git clone https://github.com/yourusername/project-muei.git
   cd project-muei
```

Create virtual environment

```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
      
   # Mac/Linux
   source venv/bin/activate
```

Install dependencies
```bash
   pip install -r requirements.txt
```

Set up environment variables

Create a .env file in the project root and add:
```bash
   ANTHROPIC_API_KEY=your_claude_api_key
   # OR
   OPENAI_API_KEY=your_openai_api_key

   # AI Provider
   AI_PROVIDER=Put_openai_or_claude

   # Twitch Configuration
   TWITCH_TOKEN=your_oauth_token
   TWITCH_CLIENT_ID=your_client_id
   TWITCH_CLIENT_SECRET=your_client_secret
   TWITCH_BOT_ID=your_bot_id
   TWITCH_CHANNEL=your_channel_name

   # TTS Configuration
   TTS_ENABLED=true
   TTS_RATE=150
   TTS_VOLUME=0.9
   
   # Bot Configuration
   RESPONSE_COOLDOWN=3
   MAX_MESSAGE_LENGTH=500
```

**Obtain credentials**

Twitch credentials

1. Create Two Twitch Accounts:
   - Bot Account: This runs the code (e.g., mybot_ai)
   - Streaming Channel: Where you broadcast (e.g., yourname)

2. Get OAuth Token:
   - Go to: https://twitchtokengenerator.com/
   - Select "Bot Chat Token"
   - Log in with your BOT account (not your streaming account)
   - Copy the OAuth token → paste into TWITCH_TOKEN in .env

3. Get Client ID & Client Secret:
   - Go to: https://dev.twitch.tv/console/apps
   - Fill in:
      - Name: Your bot name
      - OAuth Redirect URLs: http://localhost:3000
      - Category: Chat Bot
   - Click "Manage" → Copy Client ID → paste into .env
   - Click "New Secret" → Copy Client Secret → paste into .env
    
4. Get Bot User ID:
   - Go to: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
   - Enter your bot account username
   - Copy the ID → paste into TWITCH_BOT_ID in .env
  
5. Set Channel Name:
   - TWITCH_CHANNEL should be your streaming channel name (where viewers watch)

6. AI API Key

   - For Claude (Recommended):
   
      - Go to: https://console.anthropic.com/
      - Create an account → Add credits ($5 minimum)
      - Generate API key → paste into ANTHROPIC_API_KEY
      - Set AI_PROVIDER=claude

7. Set up VTube Studio
   - If you want character animation:
      - Download VTube Studio: https://denchisoft.com/
      - Open VTube Studio → Settings → General Settings
      - Enable "Start API"
      - Note the port (default: 8001)

**Personality**



## How it works

   Pipeline: 
    ```bash
    
     Twitch Chat → Message Queue → Claude/OpenAI API → AI Response
                                                         ↓
                                     ┌──────────────────┼──────────────────┐
                                     ↓                  ↓                  ↓
                               Twitch Chat          TTS Engine      VTube Studio
                              (text reply)        (voice output)    (lip-sync)
     
     ```
   1. Message Reception: Bot monitors your Twitch chat for trigger words
   2. Queueing: Messages processed one at a time to prevent overlap
   3. AI Processing: LLM generates personality-driven response
   4. Multi-Output: Response sent to chat, converted to speech, and animates character
   5. Synchronization: Waits for completion before processing next message

## What I have learnt
   - Integrating multiple real-time APIs (Twitch, LLMs, VTube Studio)
   - Asynchronous programming with Python asyncio
   - WebSocket communication and error handling
   - Message queue systems for sequential processing
   - Multi-threaded TTS processing
   - API rate limiting and reconnection logic

##  Potential Improvements
   - Upgrade TTS to ElevenLabs for better voice quality
   - Create custom fine-tuned model for character
   - Add sentiment analysis for dynamic expressions
   - Implement long-term memory
   - Rig Vtuber Model

## Credits

   - Inspired by Vedal's Neuro-sama
   - Built with Claude API / OpenAI
   - Uses VTube Studio by DenchiSoft

# Project_MEI

> **📍 STATUS:** (WIP) Basic Features added, streamable. 

This is Meibo an AI VTuber that interacts with Twitch viewers in real-time. 
Inspired by Vedal who programed the AI Vtuber on Twitch, Neuro-sama, this project demonstrates the integration of large language models, real-time chat processing, 
and character animation to create an engaging streaming experience. 

## Personality
   - Name: Meibo (nicknamed "Mei" or "Ei")
   - Character: Plague Doctor
   - Personality: Witty, sarcastic, playful, cool and composed
   - Expertise: Medical knowledge with a dark sense of humor

   - Trigger words to chat with Meibo:
      - meibo
      - mei    
      - ei
        
----- > Triggers are not case-sensitive 

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

## How it works

   Pipeline: 
   
    ```bash
    
      Twitch Chat → Message Queue → Claude/OpenAI API → AI Response
                                                     ↓
                                  ┌──────────────────┼──────────────────┐
                                  ↓                  ↓                  ↓
                            Twitch Chat          TTS Engine      VTube Studio
                            (text reply)       (voice output)     (lip-sync)
     ```
   1. Message Reception: Bot monitors your Twitch chat for trigger words
   2. Queueing: Messages processed one at a time to prevent overlap
   3. AI Processing: LLM generates personality-driven response
   4. Multi-Output: Response sent to chat, converted to speech, and animates character
   5. Synchronization: Waits for completion before processing next message

## Setup & Installation
Full setup instructions available in the Template Repository

Template Repo: https://github.com/VC-Mian/AI_VTuber

Quick Overview:

Clone the template repository

Set up Twitch credentials (bot account + streaming channel)

Obtain Claude or OpenAI API key

Configure personality in src/config.py

Run with python main.py

Prerequisites: Python 3.8+, VTube Studio, Twitch account, Claude/OpenAI API key

## What I have learnt
   - Integrating multiple real-time APIs (Twitch, LLMs, VTube Studio)
   - Asynchronous programming with Python asyncio
   - WebSocket communication and error handling
   - Message queue systems for sequential processing
   - Multi-threaded TTS processing
   - API rate limiting and reconnection logic

##  Future Improvements & integrations
   - Upgrade TTS to ElevenLabs for better voice quality
   - Create custom fine-tuned model for character
   - Add sentiment analysis for dynamic expressions
   - Implement long-term memory
   - Rig Custom Vtuber Model
   - Minecraft game play

## Challenges & Solutions

**Threading Conflicts in TTS**
- Problem: pyttsx3 "run loop already started" errors
- Solution: Create new engine instance per speech operation with proper cleanup

**VTube Studio Connection Drops**  
- Problem: WebSocket protocol errors breaking lip-sync mid-stream
- Solution: Implemented auto-reconnection with connection validation

**Message Overlap**
- Problem: Multiple concurrent chatters causing response collision
- Solution: FIFO queue system with duration-based synchronization

## Credits

   - Inspired by Vedal's Neuro-sama
   - Built with Claude API / OpenAI
   - Uses VTube Studio by DenchiSoft

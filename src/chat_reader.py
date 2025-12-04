"""
Chat Reader Module - Handles Twitch integration and message processing

This module manages:
- Connection to Twitch IRC
- Message queue for sequential processing
- Commands for moderators
- Integration with AI brain, TTS, and VTuber controller
"""

from twitchio.ext import commands
import asyncio
from queue import Queue
from src.config import Config
from src.ai_brain import AIBrain
from src.tts_engine import TTSEngine
from src.vtuber_controller import VTuberController

class MeiBot(commands.Bot):

    """Twitch bot that integrates AI and TTS"""
    
    def __init__(self):
        # Initialize the bot with Twitch credentials
        super().__init__(
            token=Config.TWITCH_TOKEN,
            client_id=Config.TWITCH_CLIENT_ID,
            client_secret=Config.TWITCH_CLIENT_SECRET,
            bot_id=Config.TWITCH_BOT_ID,
            nick=Config.TWITCH_BOT_NICK,
            prefix='!',
            initial_channels=[Config.TWITCH_CHANNEL]
        )
        
        # Initialize AI and TTS
        self.ai_brain = AIBrain()
        self.tts_engine = TTSEngine()
        
        # Initialize VTuber controller
        self.vtuber = VTuberController()
        
        # Message queue for handling multiple requests
        self.message_queue = Queue()
        self.is_processing = False
        
        # Rate limiting
        self.last_response_time = 0
        self.response_cooldown = Config.RESPONSE_COOLDOWN
        
        print(f"Mei Bot initialized! Joining channel: {Config.TWITCH_CHANNEL}")
    
    async def event_ready(self):

        """Called when the bot is ready"""

        print(f'Mei is online! Connected as {Config.TWITCH_BOT_NICK}')
        print(f'Joined channel: {Config.TWITCH_CHANNEL}')
        print(f'Waiting for messages... (Type a message in chat, mentioning the bot by its names, else you will be ignored)')
            
        # Connect to VTube Studio
        print("Connecting to VTube Studio...")
        await self.vtuber.connect()
    
    async def event_channel_joined(self, channel):
        """Called when bot successfully joins a channel"""
        print(f'✓ Bot successfully joined channel: {channel.name}')
    
    async def event_join(self, channel, user):
        """Called when someone joins the channel"""
        print(f'[JOIN] {user.name} joined {channel.name}')
    
    async def event_message(self, message):
        """Called when a message is received in chat"""
        # Ignore messages without an author (system messages)
        if not message.author:
            return
        
        print(f"[DEBUG] Received message: {message.author.name}: {message.content}")
        
        # Ignore messages from the bot itself
        if message.echo:
            print(f"[DEBUG] Ignoring echo message")
            return
        
        # Handle commands first
        await self.handle_commands(message)
        
        # Check if we should respond to this message
        if self.ai_brain.should_respond(message.content):
            print(f"[DEBUG] Message triggered AI response")
            await self.handle_ai_response(message)
        else:
            print(f"[DEBUG] Message did not trigger AI response")
    
    async def handle_ai_response(self, message):
        """Queue message for AI response"""
        # Add message to queue
        self.message_queue.put(message)
        print(f"[QUEUE] Added message to queue. Queue size: {self.message_queue.qsize()}")
        
        # Start processing if not already running
        if not self.is_processing:
            await self.process_queue()
    
    async def process_queue(self):
        """Process messages from queue one at a time"""
        self.is_processing = True
        
        while not self.message_queue.empty():
            message = self.message_queue.get()
            
            try:
                print(f"[PROCESSING] Message from {message.author.name}: {message.content}")
                
                # Generate AI response
                response = self.ai_brain.generate_response(
                    username=message.author.name,
                    message=message.content
                )
                
                if len(response) > 450:  # Leave buffer for safety
                    # Split into sentences
                    sentences = response.replace('!', '.').replace('?', '.').split('.')
                    current_message = ""
                    
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if not sentence:
                            continue
                        
                        # Add sentence if it fits
                        if len(current_message) + len(sentence) + 2 < 450:
                            current_message += sentence + ". "
                        else:
                            # Send current message and start new one
                            if current_message:
                                await message.channel.send(current_message.strip())
                                print(f"[CHAT] Response sent (part): {current_message.strip()}")
                                await asyncio.sleep(1)  # Small delay between messages
                            current_message = sentence + ". "
                    
                    # Send remaining message
                    if current_message:
                        await message.channel.send(current_message.strip())
                        print(f"[CHAT] Response sent (final): {current_message.strip()}")
                else:
                    # Short response, send as-is
                    await message.channel.send(response)
                    print(f"[CHAT] Response sent: {response}")
                
                # Speak response and animate model simultaneously
                print(f"[TTS] Speaking response...")
                self.tts_engine.speak(response)

                # Animate VTuber model while speaking
                print(f"[VTUBER] Animating mouth...")
                await self.vtuber.simulate_talking(response)
 
                # Small buffer after speaking
                await asyncio.sleep(1)
                
                # Wait for TTS to finish (estimate based on text length)
                # Roughly 150 words per minute = 2.5 words per second
                word_count = len(response.split())
                tts_duration = (word_count / 2.5) + 1  # +1 second buffer
                await asyncio.sleep(tts_duration)
                
                # Cooldown between responses
                await asyncio.sleep(self.response_cooldown)
                
                print(f"[QUEUE] Finished processing. Remaining: {self.message_queue.qsize()}")
            
            except Exception as e:
                print(f"[ERROR] Error processing message: {e}")
        
        self.is_processing = False
        print(f"[QUEUE] Queue empty, waiting for new messages")
    
    @commands.command(name='mei')
    async def mei_command(self, ctx):
        """Direct command to talk to Mei"""
        # Get everything after !mei
        message_content = ctx.message.content.replace('!mei', '', 1).strip()
        
        if not message_content:
            await ctx.send("You called? What do you need?")
            return
        
        # Process through queue system
        await self.handle_ai_response(ctx.message)
    
    @commands.command(name='clear')
    async def clear_history(self, ctx):
        """Clear conversation history"""
        # Only allow broadcaster or mods
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            self.ai_brain.clear_history()
            await ctx.send("Memory cleared! Starting fresh.")
        else:
            await ctx.send("Only mods can clear my memory, sorry!")
    
    @commands.command(name='tts')
    async def toggle_tts(self, ctx):
        """Toggle TTS on/off"""
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            status = self.tts_engine.toggle()
            state = "enabled" if status else "disabled"
            await ctx.send(f"TTS {state}")
        else:
            await ctx.send("Only mods can toggle TTS!")
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show available commands"""
        help_text = (
            "Commands: !meibo [message] - talk to me | "
            "!clear - clear memory (mods) | "
            "!tts - toggle TTS (mods) | "
            "Just mention 'mei' or 'meibo' in chat to talk!"
        )
        await ctx.send(help_text)

"""
Main Discord bot class for thread auto-lock functionality.
"""

import discord
from discord.ext import commands
import logging
import json
from config import Config
from handlers.thread_handler import ThreadHandler
from handlers.permission_handler import PermissionHandler

class ThreadLockBot(commands.Bot):
    """Discord bot for auto-locking threads based on role permissions."""
    
    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.logger = logging.getLogger(__name__)
        self.config = Config()
        self.thread_handler = ThreadHandler(self)
        self.permission_handler = PermissionHandler(self.config)
        
    async def setup_hook(self):
        """Called when the bot is starting up."""
        self.logger.info("Bot is setting up...")
        
        # Add the thread handler cog
        await self.add_cog(self.thread_handler)
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            self.logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready."""
        self.logger.info(f'{self.user} has connected to Discord!')
        self.logger.info(f'Bot is in {len(self.guilds)} guild(s)')
        
        # Log guild information for configuration
        for guild in self.guilds:
            self.logger.info(f'Guild: {guild.name} (ID: {guild.id})')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for 'lock' and 'lna' commands"
            )
        )
    
    async def on_message(self, message):
        """Handle incoming messages for lock/lna commands."""
        # Ignore messages from bots
        if message.author.bot:
            return
        
        # Check if message is in a thread
        if not isinstance(message.channel, discord.Thread):
            await self.process_commands(message)
            return
        
        # Check for lock commands
        content = message.content.lower().strip()
        if content in ['lock', 'lna']:
            # Check if user has permission
            if not self.permission_handler.has_lock_permission(message.author, message.guild):
                await message.channel.send(
                    "❌ You don't have permission to lock threads.",
                    delete_after=5
                )
                return
            
            # Handle thread locking
            await self.thread_handler.handle_lock_request(message)
        
        # Process other commands
        await self.process_commands(message)
    

    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return
        
        self.logger.error(f"Command error in {ctx.command}: {error}")
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to execute this command.")
        else:
            await ctx.send("❌ An error occurred while executing the command.")

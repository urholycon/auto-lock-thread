#!/usr/bin/env python3
"""
Main entry point for the Discord Thread Auto-Lock Bot.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from bot import ThreadLockBot
from utils.logger import setup_logger
from keep_alive import keep_alive

# Load environment variables
load_dotenv()

def main():
    """Main function to start the Discord bot."""
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please set DISCORD_TOKEN in your .env file or environment.")
        return
    
    # Create and run the bot
    try:
        # Start keep alive server BEFORE bot.run for 24/7 running
        logger.info("Starting keep-alive web server...")
        keep_alive()
        logger.info("Keep-alive server started successfully on port 8080")
        
        # Small delay to ensure web server is ready
        import time
        time.sleep(1)
        
        bot = ThreadLockBot()
        logger.info("Starting Discord Thread Lock Bot...")
        logger.info("Web interface available for monitoring and pinging")
        bot.run(token)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()

"""
Logging utilities for the Discord Thread Lock Bot.
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logger(log_level: str = "INFO", log_file: str = "bot.log") -> None:
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Get log level from environment or use default
    level = getattr(logging, os.getenv("LOG_LEVEL", log_level).upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(f"logs/{log_file}", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Set discord.py logging level to WARNING to reduce noise
    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)

def log_thread_action(action: str, thread_name: str, moderator: str, guild_name: str, 
                     additional_info: Optional[str] = None) -> None:
    """Log thread actions to both file and console."""
    logger = logging.getLogger("thread_actions")
    
    # Create action log entry
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = {
        "timestamp": timestamp,
        "action": action,
        "thread_name": thread_name,
        "moderator": moderator,
        "guild": guild_name
    }
    
    if additional_info:
        log_entry["info"] = additional_info
    
    # Format log message
    log_message = f"[{action}] Thread '{thread_name}' by {moderator} in {guild_name}"
    if additional_info:
        log_message += f" - {additional_info}"
    
    logger.info(log_message)
    
    # Also write to specific thread actions log
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/thread_actions.log", "a", encoding="utf-8") as f:
            f.write(f"{timestamp} | {log_message}\n")
    except Exception as e:
        logger.error(f"Failed to write to thread actions log: {e}")

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

class ThreadActionLogger:
    """Context manager for thread action logging."""
    
    def __init__(self, action: str, thread_name: str, moderator: str, guild_name: str):
        self.action = action
        self.thread_name = thread_name
        self.moderator = moderator
        self.guild_name = guild_name
        self.logger = logging.getLogger(__name__)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        self.logger.info(f"Starting {self.action} for thread '{self.thread_name}'")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        if exc_type is None:
            # Success
            log_thread_action(
                self.action,
                self.thread_name,
                self.moderator,
                self.guild_name,
                f"Completed in {duration:.2f}s"
            )
        else:
            # Error occurred
            self.logger.error(f"Failed {self.action} for thread '{self.thread_name}': {exc_val}")
            log_thread_action(
                f"{self.action}_FAILED",
                self.thread_name,
                self.moderator,
                self.guild_name,
                f"Error: {exc_val}"
            )

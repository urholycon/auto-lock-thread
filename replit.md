# Discord Thread Auto-Lock Bot

## Overview

This is a Discord bot built with Python and discord.py that automatically locks threads based on role permissions and provides interactive options to delete locked threads. The bot features role-based authorization, configurable settings, comprehensive logging, and a 24/7 uptime system with a Flask web server for monitoring.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular, event-driven architecture built on the discord.py framework:

**Problem**: Need a Discord bot that can automatically manage thread lifecycle with proper permission controls
**Solution**: Modular Python bot with separate handlers for different concerns (permissions, thread operations, configuration)
**Rationale**: Separation of concerns makes the codebase maintainable and allows for easy feature additions

### Core Components:
- **Event-driven Discord Bot**: Built on discord.py with async/await patterns for non-blocking operations
- **Flask Web Server**: Provides keep-alive functionality and monitoring endpoints for 24/7 uptime
- **JSON Configuration System**: File-based configuration with environment variable overrides
- **Cog-based Architecture**: Uses Discord.py's cog system for organized command and event handling

## Key Components

### Bot Infrastructure (`bot.py`, `main.py`)
- **Main Bot Class**: `ThreadLockBot` extends `commands.Bot` with custom intents and setup
- **Startup Process**: Handles cog loading, command syncing, and error handling
- **Keep-alive System**: Flask server runs alongside the bot to maintain uptime on hosting platforms

### Configuration Management (`config.py`, `config.json`)
- **JSON-based Settings**: Persistent configuration stored in `config.json`
- **Default Fallbacks**: Automatic fallback to sensible defaults if config is missing/corrupted
- **Guild-specific Overrides**: Different role configurations per Discord server
- **Environment Integration**: Discord token loaded from environment variables for security

### Permission System (`handlers/permission_handler.py`)
- **Multi-tier Authorization**: Checks administrator perms → manage_threads perms → custom roles → role IDs
- **Role Name Support**: Configurable role names per guild (e.g., "Moderator", "Staff")
- **Role ID Support**: Fallback to role IDs for more reliable permission checking
- **Debug Logging**: Comprehensive logging of all permission checks

### Thread Operations (`handlers/thread_handler.py`)
- **Command Triggers**: Responds to "lock" or "lna" commands in thread messages
- **Interactive UI**: Discord UI components (buttons) for delete/keep confirmation
- **Auto-delete Feature**: Configurable auto-deletion for specific channels
- **User Validation**: Only the locking moderator can delete threads

### Logging System (`utils/logger.py`)
- **Dual Output**: Logs to both file (`logs/bot.log`) and console
- **Action Tracking**: Dedicated logging for all thread lock/unlock/delete actions
- **Discord Library Noise Reduction**: Filters out verbose discord.py logging

## Data Flow

1. **Bot Startup**: `main.py` → loads environment → starts Flask server → initializes bot → syncs commands
2. **Message Processing**: Discord message → permission check → command detection → action execution
3. **Thread Locking**: User types "lock" → permission validation → thread.edit(locked=True) → UI buttons displayed
4. **Thread Deletion**: User clicks delete button → user validation → thread unlocked → thread deleted
5. **Logging**: All actions → formatted log entry → file + console output

## External Dependencies

### Required Packages:
- **discord.py**: Core Discord API wrapper for bot functionality
- **python-dotenv**: Environment variable loading from .env files
- **Flask**: Web server for keep-alive and monitoring endpoints

### Discord Requirements:
- **Bot Token**: Obtained from Discord Developer Portal
- **Bot Permissions**: Manage Threads, Send Messages, Read Message History
- **Gateway Intents**: Message Content, Server Members, Guilds

### Optional Integrations:
- **Log Channels**: Bot can send action logs to specified Discord channels
- **External Monitoring**: Flask endpoints (`/status`, `/ping`) for uptime monitoring

## Deployment Strategy

**Problem**: Need reliable 24/7 bot hosting with automatic restarts
**Solution**: Combination of Flask keep-alive server and environment-based configuration
**Rationale**: Many free hosting platforms sleep inactive applications; keep-alive prevents this

### Deployment Components:
1. **Automatic Dependencies**: Smart dependency checking and installation with `install_deps.py` 
2. **Environment Setup**: Discord token in environment variables or .env file
3. **Keep-alive Server**: Flask server on port 5000 provides HTTP endpoints for monitoring
4. **Auto-restart Logic**: Bot automatically restarts on crashes with full error logging
5. **Configuration Persistence**: JSON config file maintains settings across restarts
6. **Setup Automation**: Complete setup script with `setup.py` for one-command deployment

### Hosting Considerations:
- **Process Management**: Single process runs both Flask server and Discord bot
- **Port Configuration**: Flask server defaults to port 8000, configurable via environment
- **Error Handling**: Comprehensive try-catch blocks with detailed error logging
- **Graceful Shutdown**: Proper cleanup and logging on bot shutdown

The architecture prioritizes reliability, maintainability, and ease of deployment while providing a robust permission system and user-friendly interface for Discord thread management.
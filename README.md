# Discord Thread Auto-Lock Bot

A Discord bot that automatically locks threads based on role permissions and provides options to delete locked threads.

## Features

- 🔒 **Auto-lock threads** when authorized users type "lock" or "lna"
- 🗑️ **Thread deletion options** with interactive buttons after locking
- 👮 **Role-based permissions** with configurable authorized roles
- 📝 **Comprehensive logging** of all lock/unlock/delete actions
- ⚙️ **Easy configuration** with JSON config file and slash commands
- 🛡️ **Error handling** for edge cases and permission issues
- 🌐 **24/7 Uptime** with keep-alive web server

## Quick Start

### 1. Prerequisites

- Python 3.11 or higher
- A Discord bot token ([Create one here](https://discord.com/developers/applications))

### 2. Installation

#### Automatic Setup (Recommended)
```bash
python setup.py
```

#### Manual Setup
```bash
# Check and install dependencies
python install_deps.py

# Set up your Discord token
# Add DISCORD_TOKEN to your environment variables or Replit Secrets
```

**Dependencies are automatically managed:**
- discord.py ≥2.3.0
- python-dotenv ≥1.0.0  
- flask ≥3.0.0
- aiohttp ≥3.8.0
- requests ≥2.31.0

### 3. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Enable these **Privileged Gateway Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Guilds Intent
4. Get your bot token and add it to `.env`

### 4. Bot Permissions

Your bot needs these permissions in Discord servers:
- **Manage Threads** (required)
- **Send Messages** (required)
- **Read Message History** (required)
- **Use External Emojis** (optional, for better UI)

## How to Use

### Basic Thread Locking

1. In any thread, authorized users can type:
   - `lock` - Locks the thread
   - `lna` - Also locks the thread (short for "lock no archive")

2. After locking, two buttons appear:
   - 🗑️ **Delete** - Deletes the locked thread
   - 📌 **Keep** - Keeps the thread locked

### Configuration Commands

- `!lockconfig` - View current configuration
- `!lockconfig add <role_name>` - Add authorized role
- `!lockconfig remove <role_name>` - Remove authorized role  
- `!lockconfig list` - List all authorized roles
- `!unlock` - Unlock current thread (requires manage_threads permission)

### Auto-Delete Channels

Configure channels where threads auto-delete 5 seconds after locking:

1. Edit `config.json`
2. Add channel IDs to `auto_delete_channels` array:
```json
{
    "auto_delete_channels": [1234567890123456789]
}
```

## 🔍 24/7 Monitoring & Uptime

Bot ini dilengkapi sistem monitoring komprehensif untuk memastikan bot tetap online 24/7:

### Built-in Monitoring Endpoints
- **`/ping`** - Quick alive check untuk external monitors
- **`/status`** - Detailed bot status dan informasi lengkap
- **`/health`** - Simple health check endpoint
- **`/uptime`** - Statistik uptime dan metrics

### External Monitoring (Recommended)
Untuk menjamin uptime 24/7, gunakan layanan monitoring eksternal:

**🌟 UptimeRobot (Gratis & Direkomendasikan)**
1. Daftar di [uptimerobot.com](https://uptimerobot.com)
2. Tambah HTTP monitor baru
3. URL: `https://your-bot-url.replit.app/ping`
4. Interval: 5 menit

**Alternative: StatusCake, Pingdom**
Setup dengan URL dan interval yang sama untuk redundancy.

### Internal Monitor
Jalankan monitoring internal secara terpisah:
```bash
python monitor.py --url https://your-bot-url.replit.app --interval 300
```

**📖 Panduan Lengkap**: Lihat `monitoring_setup.md` untuk setup detail semua layanan monitoring.

## Web Interface

Bot menyediakan web interface untuk monitoring di `http://localhost:5000`:
- Dashboard status bot
- API endpoints untuk health check
- Statistik uptime dan ping count
- Informasi lengkap tentang fitur bot

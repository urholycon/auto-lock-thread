#!/usr/bin/env python3
"""
External Monitor for Discord Thread Auto-Lock Bot
Keeps the bot alive by making regular HTTP requests
"""
import time
import requests
import threading
import logging
from datetime import datetime

class BotMonitor:
    """External monitoring system for Discord bot uptime"""
    
    def __init__(self, bot_url="http://localhost:5000", interval=300):
        """
        Initialize bot monitor
        
        Args:
            bot_url (str): URL of the bot's web interface
            interval (int): Ping interval in seconds (default: 5 minutes)
        """
        self.bot_url = bot_url
        self.interval = interval
        self.running = False
        self.monitor_thread = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('BotMonitor')
    
    def ping_bot(self):
        """Send a ping request to the bot"""
        try:
            response = requests.get(f"{self.bot_url}/ping", timeout=10)
            if response.status_code == 200:
                self.logger.info(f"✅ Bot ping successful - Status: {response.status_code}")
                return True
            else:
                self.logger.warning(f"⚠️ Bot ping returned status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Bot ping failed: {e}")
            return False
    
    def get_bot_status(self):
        """Get detailed bot status"""
        try:
            response = requests.get(f"{self.bot_url}/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"📊 Bot Status: {data.get('status', 'unknown')}")
                return data
            else:
                self.logger.warning(f"Status check returned: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Status check failed: {e}")
            return None
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info(f"🔍 Starting bot monitor - pinging every {self.interval} seconds")
        
        while self.running:
            try:
                # Ping the bot
                success = self.ping_bot()
                
                if not success:
                    self.logger.warning("Bot ping failed, trying status check...")
                    status = self.get_bot_status()
                    if not status:
                        self.logger.error("❌ Bot appears to be down!")
                
                # Wait for next ping
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                self.logger.info("Monitor stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Monitor loop error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def start(self):
        """Start the monitoring service"""
        if self.running:
            self.logger.warning("Monitor is already running")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("🚀 Bot monitor started successfully")
    
    def stop(self):
        """Stop the monitoring service"""
        if not self.running:
            return
        
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("🛑 Bot monitor stopped")
    
    def is_running(self):
        """Check if monitor is running"""
        return self.running

def main():
    """Run the bot monitor as a standalone service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Discord Bot Monitor')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Bot URL (default: http://localhost:5000)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Ping interval in seconds (default: 300 = 5 minutes)')
    
    args = parser.parse_args()
    
    monitor = BotMonitor(bot_url=args.url, interval=args.interval)
    
    try:
        monitor.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nShutting down monitor...")
        monitor.stop()

if __name__ == "__main__":
    main()
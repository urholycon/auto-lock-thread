"""
Configuration management for the Discord Thread Lock Bot.
"""

import json
import logging
import os
from typing import Dict, List, Any

class Config:
    """Handles bot configuration loading and management."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config_data = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_file}")
                return config
            else:
                self.logger.warning(f"Config file {self.config_file} not found, using defaults")
                return self.get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing config file: {e}")
            return self.get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "authorized_roles": [
                "Moderator",
                "Admin",
                "Staff"
            ],
            "lock_commands": ["lock", "lna"],
            "auto_delete_timeout": 30,
            "log_channel_name": "thread-logs",
            "embed_color": 0xFF5733,
            "delete_confirmation_timeout": 60
        }
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def get_authorized_roles(self, guild_id: int = None) -> List[str]:
        """Get list of authorized role names."""
        if guild_id and str(guild_id) in self.config_data.get("guild_specific", {}):
            return self.config_data["guild_specific"][str(guild_id)].get("authorized_roles", 
                                                                        self.config_data["authorized_roles"])
        return self.config_data.get("authorized_roles", [])
    
    def add_authorized_role(self, role_name: str, guild_id: int = None) -> bool:
        """Add a role to authorized roles list."""
        if guild_id:
            # Guild-specific configuration
            if "guild_specific" not in self.config_data:
                self.config_data["guild_specific"] = {}
            if str(guild_id) not in self.config_data["guild_specific"]:
                self.config_data["guild_specific"][str(guild_id)] = {"authorized_roles": []}
            
            roles = self.config_data["guild_specific"][str(guild_id)]["authorized_roles"]
            if role_name not in roles:
                roles.append(role_name)
                return self.save_config()
        else:
            # Global configuration
            if role_name not in self.config_data["authorized_roles"]:
                self.config_data["authorized_roles"].append(role_name)
                return self.save_config()
        return False
    
    def remove_authorized_role(self, role_name: str, guild_id: int = None) -> bool:
        """Remove a role from authorized roles list."""
        if guild_id:
            # Guild-specific configuration
            if ("guild_specific" in self.config_data and 
                str(guild_id) in self.config_data["guild_specific"]):
                roles = self.config_data["guild_specific"][str(guild_id)]["authorized_roles"]
                if role_name in roles:
                    roles.remove(role_name)
                    return self.save_config()
        else:
            # Global configuration
            if role_name in self.config_data["authorized_roles"]:
                self.config_data["authorized_roles"].remove(role_name)
                return self.save_config()
        return False
    
    def get_setting(self, key: str, default=None):
        """Get a configuration setting."""
        return self.config_data.get(key, default)

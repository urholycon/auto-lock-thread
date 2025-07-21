"""
Permission handling for thread lock operations.
"""

import discord
import logging
from typing import List

class PermissionHandler:
    """Handles permission checking for thread lock operations."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def has_lock_permission(self, user: discord.Member, guild: discord.Guild) -> bool:
        """Check if a user has permission to lock threads."""
        # Check if user is administrator
        if user.guild_permissions.administrator:
            return True
        
        # Check if user has manage_threads permission
        if user.guild_permissions.manage_threads:
            return True
        
        # Check if user has any of the authorized roles
        authorized_roles = self.config.get_authorized_roles(guild.id)
        user_roles = [role.name for role in user.roles]
        
        for role_name in authorized_roles:
            if role_name in user_roles:
                self.logger.debug(f"User {user.name} has authorized role: {role_name}")
                return True
        
        # Check for role IDs if configured
        authorized_role_ids = self.config.get_setting("authorized_role_ids", {})
        guild_role_ids = authorized_role_ids.get(str(guild.id), [])
        user_role_ids = [role.id for role in user.roles]
        
        for role_id in guild_role_ids:
            if role_id in user_role_ids:
                self.logger.debug(f"User {user.name} has authorized role ID: {role_id}")
                return True
        
        self.logger.debug(f"User {user.name} does not have lock permissions")
        return False
    
    def get_user_roles(self, user: discord.Member) -> List[str]:
        """Get list of role names for a user."""
        return [role.name for role in user.roles if role.name != "@everyone"]
    
    def has_delete_permission(self, user: discord.Member, original_locker: discord.Member, guild: discord.Guild) -> bool:
        """Check if a user can delete a thread they didn't lock."""
        # Original locker can always delete
        if user.id == original_locker.id:
            return True
        
        # Administrators can delete any locked thread
        if user.guild_permissions.administrator:
            return True
        
        # Users with manage_threads can delete any locked thread
        if user.guild_permissions.manage_threads:
            return True
        
        return False
    
    def check_bot_permissions(self, guild: discord.Guild, bot_member: discord.Member) -> dict:
        """Check if bot has required permissions."""
        permissions = {
            "manage_threads": bot_member.guild_permissions.manage_threads,
            "send_messages": bot_member.guild_permissions.send_messages,
            "embed_links": bot_member.guild_permissions.embed_links,
            "read_message_history": bot_member.guild_permissions.read_message_history,
            "use_external_emojis": bot_member.guild_permissions.use_external_emojis
        }
        
        missing_permissions = [perm for perm, has_perm in permissions.items() if not has_perm]
        
        if missing_permissions:
            self.logger.warning(f"Bot missing permissions in {guild.name}: {missing_permissions}")
        
        return {
            "all_permissions": all(permissions.values()),
            "permissions": permissions,
            "missing": missing_permissions
        }

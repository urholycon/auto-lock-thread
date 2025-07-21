"""
Thread handling functionality for lock/unlock operations and deletion.
"""

import discord
from discord.ext import commands
import logging
import asyncio
from datetime import datetime
from utils.logger import log_thread_action

class DeleteThreadView(discord.ui.View):
    """View for thread deletion confirmation."""
    
    def __init__(self, thread: discord.Thread, moderator: discord.Member):
        super().__init__(timeout=60)
        self.thread = thread
        self.moderator = moderator
        self.logger = logging.getLogger(__name__)
    
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def delete_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle thread deletion."""
        # Check if the user clicking is the same as the one who locked it
        if interaction.user.id != self.moderator.id:
            await interaction.response.send_message(
                "❌ Only the moderator who locked this thread can delete it.", 
                ephemeral=True
            )
            return
        
        try:
            thread_name = self.thread.name
            guild_name = self.thread.guild.name
            
            await interaction.response.send_message(
                f"🗑️ Deleting thread '{thread_name}'...", 
                ephemeral=True
            )
            
            # Unlock thread first if it's locked (required for deletion)
            if self.thread.locked:
                await self.thread.edit(locked=False)
                await asyncio.sleep(0.5)
            
            # Log the deletion
            log_thread_action(
                action="DELETE",
                thread_name=thread_name,
                moderator=self.moderator.name,
                guild_name=guild_name
            )
            
            # Delete the thread
            await self.thread.delete()
            
        except discord.NotFound:
            await interaction.followup.send("❌ Thread not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I don't have permission to delete this thread.", ephemeral=True)
        except Exception as e:
            self.logger.error(f"Error deleting thread: {e}")
            await interaction.followup.send("❌ An error occurred while deleting the thread.", ephemeral=True)
    
    @discord.ui.button(label="Keep", style=discord.ButtonStyle.secondary, emoji="📌")
    async def keep_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle keeping the thread."""
        await interaction.response.send_message(
            f"📌 Thread '{self.thread.name}' will be kept locked.", 
            ephemeral=True
        )
        
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        await interaction.edit_original_response(view=self)
    
    async def on_timeout(self):
        """Handle view timeout."""
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        try:
            # Just disable the buttons without changing the message
            await self.message.edit(view=self)
        except:
            pass  # Message might have been deleted

class ThreadHandler(commands.Cog):
    """Handles thread locking, unlocking, and deletion operations."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    async def handle_lock_request(self, message: discord.Message):
        """Handle a thread lock request."""
        thread = message.channel
        
        try:
            # Check if thread is already locked
            if thread.locked:
                await message.channel.send(
                    "🔒 This thread is already locked.",
                    delete_after=5
                )
                return
            
            # Lock the thread
            await thread.edit(locked=True)
            
            # Log the action
            log_thread_action(
                action="LOCK",
                thread_name=thread.name,
                moderator=message.author.name,
                guild_name=message.guild.name
            )
            
            # Check if thread is in auto-delete channel
            auto_delete_channels = self.bot.config.get_setting("auto_delete_channels", [])
            is_auto_delete_channel = False
            
            # Check if parent channel (where thread was created) is in auto-delete list
            if thread.parent_id in auto_delete_channels:
                is_auto_delete_channel = True
            
            if is_auto_delete_channel:
                # Send message and auto-delete thread in 5 seconds
                confirmation_msg = await message.channel.send(
                    "This thread has been locked and will be deleted in 5 seconds"
                )
                
                # Wait 5 seconds then delete the thread
                await asyncio.sleep(5)
                
                try:
                    # Log the auto-deletion
                    log_thread_action(
                        action="AUTO_DELETE",
                        thread_name=thread.name,
                        moderator=message.author.name,
                        guild_name=message.guild.name,
                        additional_info="Auto-deleted from special channel"
                    )
                    
                    # Unlock thread first, then delete
                    await thread.edit(locked=False)
                    await asyncio.sleep(0.5)  # Small delay to ensure unlock is processed
                    await thread.delete()
                    
                except discord.NotFound:
                    self.logger.warning(f"Thread '{thread.name}' was already deleted")
                except discord.Forbidden:
                    self.logger.error(f"No permission to delete thread '{thread.name}'")
                except Exception as e:
                    self.logger.error(f"Error auto-deleting thread '{thread.name}': {e}")
            else:
                # Normal lock behavior with deletion options
                view = DeleteThreadView(thread, message.author)
                
                # Send simple confirmation message
                confirmation_msg = await message.channel.send(
                    "This thread has been locked",
                    view=view
                )
                
                # Store the message reference in the view for timeout handling
                view.message = confirmation_msg
            
            self.logger.info(f"Thread '{thread.name}' locked by {message.author} in {message.guild.name}")
            
        except discord.Forbidden:
            await message.channel.send(
                "❌ I don't have permission to lock this thread.",
                delete_after=5
            )
        except Exception as e:
            self.logger.error(f"Error locking thread: {e}")
            await message.channel.send(
                "❌ An error occurred while locking the thread.",
                delete_after=5
            )
    
    @commands.command(name="unlock")
    @commands.has_permissions(manage_threads=True)
    async def unlock_thread(self, ctx):
        """Unlock the current thread."""
        if not isinstance(ctx.channel, discord.Thread):
            await ctx.send("❌ This command can only be used in threads.")
            return
        
        thread = ctx.channel
        
        try:
            if not thread.locked:
                await ctx.send("🔓 This thread is not locked.")
                return
            
            # Unlock the thread
            await thread.edit(locked=False)
            
            # Log the action
            log_thread_action(
                action="UNLOCK",
                thread_name=thread.name,
                moderator=ctx.author.name,
                guild_name=ctx.guild.name
            )
            
            # Create embed for unlock confirmation
            embed = discord.Embed(
                title="🔓 Thread Unlocked",
                description=f"This thread has been unlocked by {ctx.author.mention}",
                color=0x00FF00,
                timestamp=datetime.utcnow()
            )
            
            await ctx.send(embed=embed)
            self.logger.info(f"Thread '{thread.name}' unlocked by {ctx.author} in {ctx.guild.name}")
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unlock this thread.")
        except Exception as e:
            self.logger.error(f"Error unlocking thread: {e}")
            await ctx.send("❌ An error occurred while unlocking the thread.")
    
    @commands.command(name="lockconfig")
    @commands.has_permissions(administrator=True)
    async def lock_config(self, ctx, action: str = None, *, role_name: str = None):
        """Configure thread lock settings."""
        if not action:
            # Show current configuration
            authorized_roles = self.bot.config.get_authorized_roles(ctx.guild.id)
            
            embed = discord.Embed(
                title="🔧 Thread Lock Configuration",
                color=0x3498DB
            )
            embed.add_field(
                name="Authorized Roles",
                value="\n".join(f"• {role}" for role in authorized_roles) if authorized_roles else "None",
                inline=False
            )
            embed.add_field(
                name="Commands",
                value="```\n!lockconfig add <role_name>\n!lockconfig remove <role_name>\n!lockconfig list```",
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        if action.lower() == "add" and role_name:
            success = self.bot.config.add_authorized_role(role_name, ctx.guild.id)
            if success:
                await ctx.send(f"✅ Added '{role_name}' to authorized roles.")
            else:
                await ctx.send(f"❌ '{role_name}' is already in authorized roles.")
        
        elif action.lower() == "remove" and role_name:
            success = self.bot.config.remove_authorized_role(role_name, ctx.guild.id)
            if success:
                await ctx.send(f"✅ Removed '{role_name}' from authorized roles.")
            else:
                await ctx.send(f"❌ '{role_name}' not found in authorized roles.")
        
        elif action.lower() == "list":
            authorized_roles = self.bot.config.get_authorized_roles(ctx.guild.id)
            role_list = "\n".join(f"• {role}" for role in authorized_roles) if authorized_roles else "No authorized roles configured."
            
            embed = discord.Embed(
                title="📋 Authorized Roles",
                description=role_list,
                color=0x3498DB
            )
            await ctx.send(embed=embed)
        
        else:
            await ctx.send("❌ Invalid usage. Use `!lockconfig` to see available commands.")

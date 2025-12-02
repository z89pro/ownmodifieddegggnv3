"""
Message Manager - Handles automatic deletion of non-important messages
Author: Gagan (Enhanced by AI)
"""

import asyncio
from typing import Optional, Union
from pyrogram.types import Message as PyrogramMessage
from telethon.tl.custom.message import Message as TelethonMessage

class MessageManager:
    """Manages automatic deletion of non-important messages"""
    
    # Delay configurations (in seconds)
    COMMAND_DELAY = 4      # Delete user commands quickly
    STATUS_DELAY = 4       # Delete status/processing messages
    ERROR_DELAY = 10       # Keep errors visible longer for user to read
    SUCCESS_DELAY = 8      # Delete success messages after reading
    
    @staticmethod
    async def smart_delete(client, message: Union[PyrogramMessage, TelethonMessage], delay: int = 4):
        """
        Delete message after specified delay with error handling
        
        Args:
            client: Telegram client (Pyrogram or Telethon)
            message: Message object to delete
            delay: Seconds to wait before deletion
        """
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except Exception:
            # Message already deleted or insufficient permissions
            pass
    
    @staticmethod
    def auto_delete(client, message: Union[PyrogramMessage, TelethonMessage], delay: Optional[int] = None):
        """
        Schedule message for automatic deletion (non-blocking)
        
        Args:
            client: Telegram client
            message: Message to delete
            delay: Optional custom delay (defaults to STATUS_DELAY)
        """
        if delay is None:
            delay = MessageManager.STATUS_DELAY
        asyncio.create_task(MessageManager.smart_delete(client, message, delay))
    
    @staticmethod
    def delete_command(client, message: Union[PyrogramMessage, TelethonMessage]):
        """Delete user command messages quickly"""
        MessageManager.auto_delete(client, message, MessageManager.COMMAND_DELAY)
    
    @staticmethod
    def delete_status(client, message: Union[PyrogramMessage, TelethonMessage]):
        """Delete status/processing messages"""
        MessageManager.auto_delete(client, message, MessageManager.STATUS_DELAY)
    
    @staticmethod
    def delete_error(client, message: Union[PyrogramMessage, TelethonMessage]):
        """Delete error messages (with longer delay)"""
        MessageManager.auto_delete(client, message, MessageManager.ERROR_DELAY)
    
    @staticmethod
    def delete_success(client, message: Union[PyrogramMessage, TelethonMessage]):
        """Delete success messages"""
        MessageManager.auto_delete(client, message, MessageManager.SUCCESS_DELAY)

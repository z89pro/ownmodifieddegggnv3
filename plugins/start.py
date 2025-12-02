# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram import filters
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID, FORCE_SUB, JOIN_LINK

async def subscribe(app, message):
    # Skip if FORCE_SUB is dummy or missing
    if not FORCE_SUB or FORCE_SUB == -10012345567:
        return 0
        
    try:
        user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
        if user.status == "ChatMemberStatus.BANNED":
            await message.reply_text("🚫 You are banned from the channel.")
            return 1
    except Exception as e:
        # If user not participant, show join link
        if "USER_NOT_PARTICIPANT" in str(e) or "UserNotParticipant" in str(e):
            try:
                link = await app.export_chat_invite_link(FORCE_SUB)
            except:
                link = JOIN_LINK
            
            caption = f"👋 **Welcome {message.from_user.first_name}!**\n\n⚠️ You must join our updates channel to use this bot."
            await message.reply_photo(
                photo="https://graph.org/file/d44f024a08ded19452152.jpg",
                caption=caption, 
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 Join Channel", url=link)],
                    [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{app.me.username}?start=start")]
                ])
            )
            return 1
        return 0 # Allow other errors (like bot not admin) to pass
    
    return 0

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    if await subscribe(client, message) == 1:
        return

    welcome_caption = (
        f"👋 **Hi {message.from_user.first_name}!**\n\n"
        "I am a **Restricted Content Saver Bot**.\n"
        "I can download videos/audio from YouTube, Instagram, and more!\n\n"
        "**Usage:**\n"
        "🔹 Send `/dl <link>` for Video\n"
        "🔹 Send `/adl <link>` for Audio\n"
        "🔹 Send `/batch` for bulk saving"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url=JOIN_LINK)],
        [InlineKeyboardButton("🆘 Support", url="https://t.me/kingofpatal")]
    ])

    await message.reply_photo(
        photo="https://graph.org/file/d44f024a08ded19452152.jpg",
        caption=welcome_caption,
        reply_markup=buttons
    )

@app.on_message(filters.command("set"))
async def set_commands(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("❌ Owner only.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start"),
        BotCommand("dl", "💀 Video Download"),
        BotCommand("adl", "🎵 Audio Download"),
        BotCommand("batch", "📦 Bulk Save"),
        BotCommand("login", "🔑 Login"),
        BotCommand("logout", "🚪 Logout"),
        BotCommand("settings", "⚙️ Settings")
    ])
    await message.reply("✅ Commands updated!")

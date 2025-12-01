# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram import filters
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID, FORCE_SUB, JOIN_LINK

async def subscribe(app, message):
    # If FORCE_SUB is not set or is the default dummy ID, skip the check
    if not FORCE_SUB or FORCE_SUB == -10012345567:
        return 0
        
    try:
        user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
        if user.status == "ChatMemberStatus.BANNED":
            await message.reply_text("🚫 You are banned from the channel. Contact Admin.")
            return 1
    except Exception as e:
        # If user is not a participant, or any other error (like channel not found), show join link
        # We only return 1 (block) if we are sure they need to join and haven't.
        # If the channel is invalid, we shouldn't block the user, but for now we assume it's a join request.
        
        # Check if the error is strictly about not being a participant
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
        
        # If the error is CHANNEL_INVALID (dummy ID), we just let them pass (return 0)
        if "CHANNEL_INVALID" in str(e) or "400" in str(e):
            return 0
            
        print(f"Subscription Check Error: {e}")
        return 0 # Default to allowing access if check fails technically
    
    return 0

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    # Check subscription first
    if await subscribe(client, message) == 1:
        return

    welcome_caption = (
        f"👋 **Hi {message.from_user.first_name}!**\n\n"
        "I am a **Restricted Content Saver Bot**.\n"
        "I can save posts from channels or groups where forwarding is off.\n"
        "I can also download videos/audio from YouTube, Instagram, and more.\n\n"
        "**How to use:**\n"
        "1. Send me a link to a public post.\n"
        "2. For private channels, use /login.\n"
        "3. Send /help for more commands."
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
        await message.reply("❌ You are not authorized to use this command.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Log in for private channels"),
        BotCommand("logout", "🚪 Log out"),
        BotCommand("dl", "💀 Download Video (YT/Insta)"),
        BotCommand("adl", "👻 Download Audio"),
        BotCommand("settings", "⚙️ Personalize"),
        BotCommand("plan", "🗓️ Premium Plans"),
        BotCommand("help", "❓ Help Guide"),
        BotCommand("cancel", "🚫 Cancel process")
    ])
 
    await message.reply("✅ Commands configured successfully!")

@app.on_message(filters.command("help"))
async def help_command(client, message):
    if await subscribe(client, message) == 1:
        return
    
    help_text = (
        "📝 **Bot Commands Guide**:\n\n"
        "🔹 **/login** - Login to Telegram (Required for Private Channels)\n"
        "🔹 **/batch** - Bulk save (Send `https://t.me/c/xxxx/1`)\n"
        "🔹 **/dl <link>** - Download Video from YouTube/Insta\n"
        "🔹 **/adl <link>** - Download Audio from YouTube\n"
        "🔹 **/settings** - Configure thumbnail, caption, etc.\n"
        "🔹 **/cancel** - Stop current operation\n\n"
        "**Note:** For private channels, you must be a member of that channel and logged in via /login."
    )
    await message.reply(help_text)

@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "📜 **Terms of Service**\n\n"
        "1. We are not responsible for content you download.\n"
        "2. Do not use this bot for copyright infringement.\n"
        "3. Admins reserve the right to ban users."
    )
    await message.reply_text(terms_text)

@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = "💰 **Premium Plan**\n\nContact Admin for pricing and limits."
    await message.reply_text(plan_text)

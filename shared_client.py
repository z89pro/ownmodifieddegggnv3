# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import os
import sys

client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    print("Starting clients ...")
    try:
        if not client.is_connected():
            await client.start(bot_token=BOT_TOKEN)
            print("SpyLib started...")
    except Exception as e:
        print(f"❌ Failed to start Telethon Client: {e}")
        os._exit(1)

    if STRING:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            print(f"⚠️ Userbot Session Invalid: {e}")
            os._exit(1)
    
    try:
        await app.start()
        print("Pyro App Started...")
    except Exception as e:
        print(f"❌ Failed to start Pyrogram Client: {e}")
        os._exit(1)
        
    return client, app, userbot

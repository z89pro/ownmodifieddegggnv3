# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import sys

client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

from telethon.errors import FloodWaitError, AccessTokenInvalidError

async def start_client():
    print("Starting clients ...")
    if not client.is_connected():
        try:
            await client.start(bot_token=BOT_TOKEN)
            print("SpyLib started...")
        except FloodWaitError as e:
            print(f"\n❌ CRITICAL ERROR: Your Bot Token is FloodWaited!\n"
                  f"You must wait {e.seconds} seconds or regenerate the token via @BotFather.\n"
                  f"Please regenerate the token and update BOT_TOKEN in Koyeb.\n")
            sys.exit(1)
        except AccessTokenInvalidError:
            print("\n❌ CRITICAL ERROR: Invalid Bot Token!\n"
                  "The BOT_TOKEN provided is invalid or has been revoked.\n"
                  "Please regenerate the token via @BotFather and update it in Koyeb.\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error starting Telethon client: {e}\n")
            sys.exit(1)

    if STRING:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            print(f"Hey honey!! check your premium string session, it may be invalid of expire {e}")
            sys.exit(1)
    
    try:
        await app.start()
        print("Pyro App Started...")
    except Exception as e:
        print(f"Error starting Pyrogram client: {e}")
        sys.exit(1)
        
    return client, app, userbot


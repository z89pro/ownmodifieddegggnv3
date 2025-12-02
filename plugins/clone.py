# plugins/clone.py

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from shared_client import app
from utils.func import get_user_data
from pyrogram.types import Message

# State Management for Clone
CLONE_STATE = {}

@app.on_message(filters.command("clone"))
async def clone_start(client, message):
    uid = message.from_user.id
    CLONE_STATE[uid] = {"step": 1}
    await message.reply_text(
        "🚀 **Clone Mode Activated**\n\n"
        "This tool will copy messages directly from Source to Target without downloading.\n"
        "• Works for Public Channels (No Login needed)\n"
        "• Works for Private Channels (Login Required)\n\n"
        "👉 **Step 1:** Send the **Source Channel ID** (e.g., -100xxxx or username)"
    )

@app.on_message(filters.private & filters.text & ~filters.command(["clone", "cancel"]))
async def clone_handler(client, message):
    uid = message.from_user.id
    if uid not in CLONE_STATE:
        return
    
    # DYNAMIC IMPORT to avoid circular dependency with batch.py
    from plugins.batch import get_uclient, get_ubot
    
    state = CLONE_STATE[uid]
    step = state["step"]
    text = message.text.strip()

    # --- STEP 1: GET SOURCE CHANNEL ---
    if step == 1:
        try:
            if text.startswith("-100"):
                source_id = int(text)
            elif text.isdigit():
                source_id = int("-100" + text)
            else:
                source_id = text # Username
            
            CLONE_STATE[uid]["source"] = source_id
            CLONE_STATE[uid]["step"] = 2
            await message.reply_text("✅ Source Set.\n\n👉 **Step 2:** Send the **First Message ID** (e.g., 1001) or Link.")
        except ValueError:
            await message.reply_text("❌ Invalid ID. Please send numeric ID (e.g. -100xxxx).")

    # --- STEP 2: GET FIRST MSG ID ---
    elif step == 2:
        try:
            if "/" in text:
                msg_id = int(text.split("/")[-1])
            else:
                msg_id = int(text)
            
            CLONE_STATE[uid]["start_id"] = msg_id
            CLONE_STATE[uid]["step"] = 3
            await message.reply_text("✅ Start ID Set.\n\n👉 **Step 3:** Send the **Last Message ID** (e.g., 1050) or Link.")
        except ValueError:
             await message.reply_text("❌ Invalid ID. Send a number.")

    # --- STEP 3: GET LAST MSG ID ---
    elif step == 3:
        try:
            if "/" in text:
                msg_id = int(text.split("/")[-1])
            else:
                msg_id = int(text)
            
            if msg_id < CLONE_STATE[uid]["start_id"]:
                await message.reply_text("❌ Last ID cannot be smaller than Start ID.")
                return

            CLONE_STATE[uid]["end_id"] = msg_id
            CLONE_STATE[uid]["step"] = 4
            await message.reply_text("✅ End ID Set.\n\n👉 **Step 4:** Send the **Target Channel ID** where you want to send files (Bot must be admin).")
        except ValueError:
             await message.reply_text("❌ Invalid ID.")

    # --- STEP 4: START CLONING ---
    elif step == 4:
        try:
            if text.startswith("-100"):
                target_id = int(text)
            else:
                target_id = int("-100" + text) if text.isdigit() else text
            
            source_id = CLONE_STATE[uid]["source"]
            
            uc = await get_uclient(uid) # User Client
            worker = client # Default to Bot
            mode = "BOT (Public)"

            if uc:
                worker = uc
                mode = "USERBOT (Private/Public)"
            
            status = await message.reply_text(f"⚙️ **Starting Clone**\nMode: {mode}\nRange: {CLONE_STATE[uid]['start_id']} - {CLONE_STATE[uid]['end_id']}")
            
            total = CLONE_STATE[uid]["end_id"] - CLONE_STATE[uid]["start_id"] + 1
            success = 0
            fail = 0
            
            for i, msg_id in enumerate(range(CLONE_STATE[uid]["start_id"], CLONE_STATE[uid]["end_id"] + 1)):
                try:
                    msg = await worker.get_messages(source_id, msg_id)
                    
                    if msg and not msg.empty:
                        try:
                            # Try bot copy first
                            await client.copy_message(
                                chat_id=target_id,
                                from_chat_id=source_id,
                                message_id=msg_id
                            )
                        except Exception:
                            # Fallback to Userbot copy
                            await worker.copy_message(chat_id=target_id, from_chat_id=source_id, message_id=msg_id)
                        
                        success += 1
                        await asyncio.sleep(2) # Safe delay
                    else:
                        fail += 1
                        
                except FloodWait as e:
                    await asyncio.sleep(e.value + 5)
                except Exception as e:
                    fail += 1
                    print(f"Clone Error {msg_id}: {e}")

                if i % 10 == 0:
                    try: await status.edit(f"🔄 Cloning... {i}/{total}\n✅ {success} | ❌ {fail}")
                    except: pass
            
            await status.edit(f"✅ **Clone Complete!**\nTotal: {total}\nSuccess: {success}\nFailed/Skipped: {fail}")
            del CLONE_STATE[uid]

        except Exception as e:
            await message.reply_text(f"❌ Critical Error: {e}")
            del CLONE_STATE[uid]

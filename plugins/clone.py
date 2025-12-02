# plugins/clone.py

import asyncio
import logging
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
    
    # Check if user is in cloning mode
    if uid not in CLONE_STATE:
        return

    try:
        # Dynamic Import to prevent circular errors
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
                    # Username handling
                    if "/" in text:
                        source_id = text.split("/")[-1]
                    else:
                        source_id = text
                
                CLONE_STATE[uid]["source"] = source_id
                CLONE_STATE[uid]["step"] = 2
                await message.reply_text(f"✅ Source Set: `{source_id}`\n\n👉 **Step 2:** Send the **First Message ID** (e.g., 1001) or Link.")
            except Exception as e:
                await message.reply_text(f"❌ Invalid ID format. Error: {e}")

        # --- STEP 2: GET FIRST MSG ID ---
        elif step == 2:
            try:
                if "/" in text:
                    msg_id = int(text.split("/")[-1])
                else:
                    msg_id = int(text)
                
                CLONE_STATE[uid]["start_id"] = msg_id
                CLONE_STATE[uid]["step"] = 3
                await message.reply_text(f"✅ Start ID: `{msg_id}`\n\n👉 **Step 3:** Send the **Last Message ID** (e.g., 1050) or Link.")
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
                await message.reply_text(f"✅ End ID: `{msg_id}`\n\n👉 **Step 4:** Send the **Target Channel ID** (Destination) where files will be copied.\n⚠️ Make sure the Bot/Userbot is Admin there.")
            except ValueError:
                 await message.reply_text("❌ Invalid ID.")

        # --- STEP 4: START CLONING ---
        elif step == 4:
            try:
                if text.startswith("-100"):
                    target_id = int(text)
                elif text.isdigit():
                    target_id = int("-100" + text)
                else:
                    target_id = text
                
                source_id = CLONE_STATE[uid]["source"]
                
                # Setup Clients
                uc = await get_uclient(uid)
                worker = uc if uc else client
                worker_name = "Userbot" if uc else "Bot"
                
                status = await message.reply_text(f"⚙️ **Initializing Clone**\nWorker: {worker_name}\nSource: {source_id}\nTarget: {target_id}")
                
                start_id = CLONE_STATE[uid]["start_id"]
                end_id = CLONE_STATE[uid]["end_id"]
                total = end_id - start_id + 1
                success = 0
                fail = 0
                
                # CLONING LOOP
                for i, msg_id in enumerate(range(start_id, end_id + 1)):
                    try:
                        # Attempt to Copy
                        # Using copy_message is safer and faster than forward_messages
                        await worker.copy_message(
                            chat_id=target_id,
                            from_chat_id=source_id,
                            message_id=msg_id
                        )
                        success += 1
                        await asyncio.sleep(2) # Delay to prevent floodwait
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 5)
                        # Retry once after floodwait
                        try:
                            await worker.copy_message(chat_id=target_id, from_chat_id=source_id, message_id=msg_id)
                            success += 1
                        except:
                            fail += 1
                    except Exception as e:
                        fail += 1
                        print(f"Clone Fail {msg_id}: {e}")

                    # Update status every 10 messages
                    if i % 10 == 0:
                        try: await status.edit(f"🔄 Cloning... {i}/{total}\n✅ Success: {success}\n❌ Skipped: {fail}")
                        except: pass
                
                await status.edit(f"✅ **Clone Completed!**\nTotal: {total}\nSuccess: {success}\nFailed/Skipped: {fail}")
                
                # Cleanup
                if uid in CLONE_STATE:
                    del CLONE_STATE[uid]

            except Exception as e:
                await message.reply_text(f"❌ Critical Clone Error: {e}")
                if uid in CLONE_STATE:
                    del CLONE_STATE[uid]

    except Exception as e:
        # Catch global errors inside handler
        await message.reply_text(f"⚠️ Error: {e}")
        print(f"Clone Handler Error: {e}")

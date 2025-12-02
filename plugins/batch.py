# plugins/batch.py - Updated with FloodWait Retry & 15s Delay

import os, re, time, asyncio, json
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from config import API_ID, API_HASH, LOG_GROUP, STRING, FREEMIUM_LIMIT, PREMIUM_LIMIT
from utils.func import E, get_user_data_key, is_premium_user
from shared_client import app as X
from plugins.batch import get_msg, process_msg, get_ubot, get_uclient, is_user_active, add_active_batch, update_batch_progress, remove_active_batch, should_cancel, Z, UB, batch_temp
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.message_manager import MessageManager

# ... (बाकी imports वही रहेंगे, बस main logic नीचे बदल रहा हूँ) ...

@X.on_message(filters.command(['batch', 'single']))
async def process_cmd(c, m):
    # Auto-delete user command
    MessageManager.delete_command(c, m)
    
    uid = m.from_user.id
    cmd = m.command[0]
    
    if FREEMIUM_LIMIT == 0 and not await is_premium_user(uid):
        msg = await m.reply_text("This bot does not provide free servies, get subscription from OWNER")
        MessageManager.delete_error(c, msg)
        return
    
    # ... (Start Checks Code same as before) ...
    
    if is_user_active(uid):
        await pro.edit('You have an active task. Use /stop to cancel it.')
        return
    
    ubot = await get_ubot(uid)
    if not ubot:
        await pro.edit('Add your bot with /setbot first')
        return
    
    Z[uid] = {'step': 'start' if cmd == 'batch' else 'start_single'}
    await pro.edit(f'Send {"start link..." if cmd == "batch" else "link you to process"}.')

# ... (Cancel Handler Same as before) ...

@X.on_message(filters.text & filters.private & ~filters.command(['start', 'batch', 'cancel', 'login', 'logout', 'stop', 'set', 'pay', 'plan', 'clone', 'redeem', 'gencode', 'single', 'setbot', 'rembot']))
async def text_handler(c, m):
    uid = m.from_user.id
    if uid not in Z: return
    s = Z[uid].get('step')
    
    # ... (Step Start and Start_Single logic same as before) ...
    
    if s == 'count':
        if not m.text.isdigit():
            await m.reply_text('Enter valid number.')
            return
        
        count = int(m.text)
        maxlimit = PREMIUM_LIMIT if await is_premium_user(uid) else FREEMIUM_LIMIT

        if count > maxlimit:
            await m.reply_text(f'Maximum limit is {maxlimit}.')
            return

        Z[uid].update({'step': 'process', 'did': str(m.chat.id), 'num': count})
        i, s, n, lt = Z[uid]['cid'], Z[uid]['sid'], Z[uid]['num'], Z[uid]['lt']
        success = 0

        uc = await get_uclient(uid)
        ubot = UB.get(uid)
        
        if not uc or not ubot:
            await m.reply_text('Missing client setup')
            Z.pop(uid, None)
            return
            
        refresh_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 REFRESH STATUS", callback_data=f"refresh_status_BATCH")]])
        smsg = await m.reply_text("**🔄 INITIALIZING BATCH...**", reply_markup=refresh_btn)
        batch_start_time = time.time()

        await add_active_batch(uid, {
            "total": n,
            "current": 0,
            "success": 0,
            "cancel_requested": False,
            "progress_message_id": smsg.id
        })
        
        try:
            for j in range(n):
                if should_cancel(uid):
                    await smsg.edit(f'Cancelled at {j}/{n}. Success: {success}')
                    break
                
                await update_batch_progress(uid, j, success)
                mid = int(s) + j
                
                # --- RETRY LOGIC FOR FLOODWAIT ---
                max_retries = 2
                retry_count = 0
                
                while retry_count <= max_retries:
                    try:
                        msg = await get_msg(ubot, uc, i, mid, lt)
                        if msg:
                            try: await smsg.edit(f"**🔄 PROCESSING: {j+1}/{n}**", reply_markup=refresh_btn)
                            except: pass
                            
                            # Processing Message
                            res = await process_msg(ubot, uc, msg, str(m.chat.id), lt, uid, i, smsg=smsg, batch_start_time=batch_start_time, processed=j+1, total=n, task_type="BATCH")
                            
                            if 'Done' in res or 'Copied' in res or 'Sent' in res:
                                success += 1
                                # --- 15 SECONDS WAIT AFTER SUCCESSFUL UPLOAD ---
                                await asyncio.sleep(15) 
                        else:
                            print(f"Skipping message {mid}, not found.")
                        
                        break # Break retry loop if successful

                    except FloodWait as e:
                        wait_time = e.value + 5
                        print(f"⚠️ FloodWait Detected: Sleeping for {wait_time} seconds. Retry {retry_count+1}/{max_retries}")
                        await smsg.edit(f"⚠️ FloodWait: {wait_time}s. Retry {retry_count+1}...")
                        await asyncio.sleep(wait_time)
                        retry_count += 1
                        if retry_count > max_retries:
                            print(f"❌ Max retries reached for message {mid}")
                    
                    except Exception as e:
                        print(f"Error in batch loop: {e}")
                        break # Other errors, move to next message

                # ----------------------------------
            
            if j+1 == n:
                await m.reply_text(f'Batch Completed ✅ Success: {success}/{n}')
        
        finally:
            await remove_active_batch(uid)
            Z.pop(uid, None)
            unique_key = f"{uid}_BATCH"
            if unique_key in batch_temp.PROGRESS_DATA: del batch_temp.PROGRESS_DATA[unique_key]

# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os, re, time, asyncio, json, asyncio 
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from config import API_ID, API_HASH, LOG_GROUP, STRING, FORCE_SUB, FREEMIUM_LIMIT, PREMIUM_LIMIT
from utils.func import get_user_data, screenshot, thumbnail, get_video_metadata
from utils.func import get_user_data_key, process_text_with_rules, is_premium_user, E
from shared_client import app as X
from plugins.settings import rename_file
from plugins.start import subscribe as sub
from utils.custom_filters import login_in_progress
from utils.encrypt import dcs
from utils.encrypt import dcs
from typing import Dict, Any, Optional
from utils.progress import batch_temp, progress_bar, humanbytes, TimeFormatter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
import math


Y = None if not STRING else __import__('shared_client').userbot
Z, P, UB, UC, emp = {}, {}, {}, {}, {}

ACTIVE_USERS = {}
ACTIVE_USERS_FILE = "active_users.json"

# fixed directory file_name problems 
def sanitize(filename):
    return re.sub(r'[<>:"/\\|?*\']', '_', filename).strip(" .")[:255]

def load_active_users():
    try:
        if os.path.exists(ACTIVE_USERS_FILE):
            with open(ACTIVE_USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

async def save_active_users_to_file():
    try:
        with open(ACTIVE_USERS_FILE, 'w') as f:
            json.dump(ACTIVE_USERS, f)
    except Exception as e:
        print(f"Error saving active users: {e}")

async def add_active_batch(user_id: int, batch_info: Dict[str, Any]):
    ACTIVE_USERS[str(user_id)] = batch_info
    await save_active_users_to_file()

def is_user_active(user_id: int) -> bool:
    return str(user_id) in ACTIVE_USERS

async def update_batch_progress(user_id: int, current: int, success: int):
    if str(user_id) in ACTIVE_USERS:
        ACTIVE_USERS[str(user_id)]["current"] = current
        ACTIVE_USERS[str(user_id)]["success"] = success
        await save_active_users_to_file()

async def request_batch_cancel(user_id: int):
    if str(user_id) in ACTIVE_USERS:
        ACTIVE_USERS[str(user_id)]["cancel_requested"] = True
        await save_active_users_to_file()
        return True
    return False

def should_cancel(user_id: int) -> bool:
    user_str = str(user_id)
    return user_str in ACTIVE_USERS and ACTIVE_USERS[user_str].get("cancel_requested", False)

async def remove_active_batch(user_id: int):
    if str(user_id) in ACTIVE_USERS:
        del ACTIVE_USERS[str(user_id)]
        await save_active_users_to_file()

def get_batch_info(user_id: int) -> Optional[Dict[str, Any]]:
    return ACTIVE_USERS.get(str(user_id))

ACTIVE_USERS = load_active_users()

ACTIVE_USERS = load_active_users()

@X.on_callback_query(filters.regex("^refresh_status_"))
async def refresh_status_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    try:
        task_type_req = query.data.split("_")[-1] 
        unique_key = f"{user_id}_{task_type_req}"
        data = batch_temp.PROGRESS_DATA.get(unique_key)
    except:
        return await query.answer("⚠️ Data Error!", show_alert=True)
    
    if not data:
        return await query.answer("⚠️ Task Stopped/Completed!", show_alert=True)
    
    percentage = data["percentage"]
    bar_length = 10
    filled_length = math.floor((percentage / 100) * bar_length)
    filled = "●"
    empty = "○"
    bar = (filled * filled_length) + (empty * (bar_length - filled_length))
    
    type_str = data["type"].upper()
    name_str = data["file_name"][:25].upper() + "..." if len(data["file_name"]) > 25 else data["file_name"].upper()
    processed_size = humanbytes(data["current"]).upper()
    total_size = humanbytes(data["total"]).upper()
    speed_str = f"{humanbytes(data['speed'])}/S".upper()
    eta_str = TimeFormatter(data['eta'] * 1000).upper()
    
    total_elapsed = time.time() - data["batch_start"]
    elapsed_str = TimeFormatter(total_elapsed * 1000).upper()
    
    stats = (
        f"╭━━━━━━━━━━━━━━━━━➣\n"
        f"┣⪼ 📦 𝗕𝗔𝗧𝗖𝗛 : {data['processed']} / {data['total_msgs']}\n"
        f"┣⪼ 📥 𝗧𝗔𝗦𝗞 : {type_str}\n"
        f"┃      {bar} ({percentage:.1f}%)\n"
        f"┃ 📂 {name_str}\n"
        f"┣⪼ ⚡ 𝗦𝗣𝗘𝗘𝗗 ➠ {speed_str}\n"
        f"┣⪼ 🗂️ 𝗦𝗜𝗭𝗘 ➠ {processed_size} / {total_size}\n"
        f"┣⪼ ⏳ 𝗘𝗧𝗔 ➠ {eta_str}\n"
        f"┣⪼ ⏱ 𝗘𝗟𝗔𝗣𝗦𝗘𝗗 ➠ {elapsed_str}\n"
        f"╰━━━┫ 𝗭 𝗔 𝗜 𝗡 ┣━━━➣"
    )
    
    try:
        await query.edit_message_text(stats, reply_markup=query.message.reply_markup)
        await query.answer("✅ Updated!")
    except MessageNotModified:
        await query.answer("⚠️ No Updates!", show_alert=False)
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

async def upd_dlg(c):
    try:
        async for _ in c.get_dialogs(limit=100): pass
        return True
    except Exception as e:
        print(f'Failed to update dialogs: {e}')
        return False

# fixed the old group of 2021-2022 extraction 🌝 (buy krne ka fayda nhi ab old group) ✅ 
async def get_msg(c, u, i, d, lt):
    try:
        if lt == 'public':
            try:
                if str(i).lower().endswith('bot'):
                    emp[i] = False
                    xm = await u.get_messages(i, d)
                    emp[i] = getattr(xm, "empty", False)
                    if not emp[i]:
                        emp[i] = True
                        print(f"Bot chat found successfully...")
                        return xm
                    
                if emp[i]:
                    xm = await c.get_messages(i, d)
                    print(f"fetched by {c.me.username}")
                    emp[i] = getattr(xm, "empty", False)
                    if emp[i]:
                        print(f"Not fetched by {c.me.username}")
                        try: await u.join_chat(i)
                        except: pass
                        xm = await u.get_messages((await u.get_chat(f"@{i}")).id, d)
                    
                    return xm                   
            except Exception as e:
                print(f'Error fetching public message: {e}')
                return None
        else:
            if u:
                try:
                    async for _ in u.get_dialogs(limit=50): pass
                    
                    # Try with -100 prefix first
                    if str(i).startswith('-100'):
                        chat_id_100 = i
                        # For - prefix, remove -100 and add just -
                        base_id = str(i)[4:]  # Remove -100
                        chat_id_dash = f"-{base_id}"
                    elif i.isdigit():
                        chat_id_100 = f"-100{i}"
                        chat_id_dash = f"-{i}"
                    else:
                        chat_id_100 = i
                        chat_id_dash = i
                    
                    # Try -100 format first
                    try:
                        result = await u.get_messages(chat_id_100, d)
                        if result and not getattr(result, "empty", False):
                            return result
                    except Exception:
                        pass
                    
                    # Try - format second
                    try:
                        result = await u.get_messages(chat_id_dash, d)
                        if result and not getattr(result, "empty", False):
                            return result
                    except Exception:
                        pass
                    
                    # Final fallback - refresh dialogs and try original
                    try:
                        async for _ in u.get_dialogs(limit=200): pass
                        result = await u.get_messages(i, d)
                        if result and not getattr(result, "empty", False):
                            return result
                    except Exception:
                        pass
                    
                    return None
                            
                except Exception as e:
                    print(f'Private channel error: {e}')
                    return None
            return None
    except Exception as e:
        print(f'Error fetching message: {e}')
        return None


async def get_ubot(uid):
    bt = await get_user_data_key(uid, "bot_token", None)
    if not bt: return None
    if uid in UB: return UB.get(uid)
    try:
        bot = Client(f"user_{uid}", bot_token=bt, api_id=API_ID, api_hash=API_HASH)
        await bot.start()
        UB[uid] = bot
        return bot
    except Exception as e:
        print(f"Error starting bot for user {uid}: {e}")
        return None

async def get_uclient(uid):
    ud = await get_user_data(uid)
    ubot = UB.get(uid)
    cl = UC.get(uid)
    if cl: return cl
    if not ud: return ubot if ubot else None
    xxx = ud.get('session_string')
    if xxx:
        try:
            ss = dcs(xxx)
            gg = Client(f'{uid}_client', api_id=API_ID, api_hash=API_HASH, device_model="v3saver", session_string=ss)
            await gg.start()
            await upd_dlg(gg)
            UC[uid] = gg
            return gg
        except Exception as e:
            print(f'User client error: {e}')
            return ubot if ubot else Y
    return Y



async def send_direct(c, m, tcid, ft=None, rtmid=None):
    try:
        if m.video:
            await c.send_video(tcid, m.video.file_id, caption=ft, duration=m.video.duration, width=m.video.width, height=m.video.height, reply_to_message_id=rtmid)
        elif m.video_note:
            await c.send_video_note(tcid, m.video_note.file_id, reply_to_message_id=rtmid)
        elif m.voice:
            await c.send_voice(tcid, m.voice.file_id, reply_to_message_id=rtmid)
        elif m.sticker:
            await c.send_sticker(tcid, m.sticker.file_id, reply_to_message_id=rtmid)
        elif m.audio:
            await c.send_audio(tcid, m.audio.file_id, caption=ft, duration=m.audio.duration, performer=m.audio.performer, title=m.audio.title, reply_to_message_id=rtmid)
        elif m.photo:
            photo_id = m.photo.file_id if hasattr(m.photo, 'file_id') else m.photo[-1].file_id
            await c.send_photo(tcid, photo_id, caption=ft, reply_to_message_id=rtmid)
        elif m.document:
            await c.send_document(tcid, m.document.file_id, caption=ft, file_name=m.document.file_name, reply_to_message_id=rtmid)
        else:
            return False
        return True
    except Exception as e:
        print(f'Direct send error: {e}')
        return False

async def process_msg(c, u, m, d, lt, uid, i, smsg=None, batch_start_time=None, processed=0, total=0, task_type="SINGLE"):
    try:
        cfg_chat = await get_user_data_key(d, 'chat_id', None)
        tcid = d
        rtmid = None
        if cfg_chat:
            if '/' in cfg_chat:
                parts = cfg_chat.split('/', 1)
                tcid = int(parts[0])
                rtmid = int(parts[1]) if len(parts) > 1 else None
            else:
                tcid = int(cfg_chat)
        
        if m.media:
            orig_text = m.caption.markdown if m.caption else ''
            proc_text = await process_text_with_rules(d, orig_text)
            user_cap = await get_user_data_key(d, 'caption', '')
            ft = f'{proc_text}\n\n{user_cap}' if proc_text and user_cap else user_cap if user_cap else proc_text
            
            if lt == 'public' and not emp.get(i, False):
                await send_direct(c, m, tcid, ft, rtmid)
                return 'Sent directly.'
            
            st = time.time()
            # p = await c.send_message(d, 'Downloading...') # Replaced by smsg

            c_name = f"{time.time()}"
            file_name = "File"
            if m.video:
                file_name = m.video.file_name
                if not file_name:
                    file_name = f"{time.time()}.mp4"
                    c_name = sanitize(file_name)
                else:
                    c_name = sanitize(file_name)
            elif m.audio:
                file_name = m.audio.file_name
                if not file_name:
                    file_name = f"{time.time()}.mp3"
                    c_name = sanitize(file_name)
                else:
                    c_name = sanitize(file_name)
            elif m.document:
                file_name = m.document.file_name
                if not file_name:
                    file_name = f"{time.time()}"
                    c_name = sanitize(file_name)
                else:
                    c_name = sanitize(file_name)
            elif m.photo:
                file_name = f"{time.time()}.jpg"
                c_name = sanitize(file_name)
            
            if not batch_start_time:
                batch_start_time = time.time()
            
            if not smsg:
                 refresh_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 REFRESH STATUS", callback_data=f"refresh_status_{task_type}")]])
                 smsg = await c.send_message(d, "**🔄 INITIALIZING TASK...**", reply_markup=refresh_btn)

            progress_args = [c, smsg, time.time(), "DOWNLOADING", c_name, processed, total, batch_start_time, uid, task_type]

            f = await u.download_media(m, file_name=c_name, progress=progress_bar, progress_args=progress_args)
            
            if not f:
                # await c.edit_message_text(d, p.id, 'Failed.')
                return 'Failed.'
            
            # await c.edit_message_text(d, p.id, 'Renaming...')
            if (
                (m.video and m.video.file_name) or
                (m.audio and m.audio.file_name) or
                (m.document and m.document.file_name)
            ):
                f = await rename_file(f, d, smsg) # Passed smsg instead of p
            
            fsize = os.path.getsize(f) / (1024 * 1024 * 1024)
            th = thumbnail(d)
            
            if fsize > 2 and Y:
                st = time.time()
                # await c.edit_message_text(d, p.id, 'File is larger than 2GB. Using alternative method...')
                await upd_dlg(Y)
                mtd = await get_video_metadata(f)
                dur, h, w = mtd['duration'], mtd['width'], mtd['height']
                th = await screenshot(f, dur, d)
                
                send_funcs = {'video': Y.send_video, 'video_note': Y.send_video_note, 
                            'voice': Y.send_voice, 'audio': Y.send_audio, 
                            'photo': Y.send_photo, 'document': Y.send_document}
                
                p_args = [c, smsg, time.time(), "UPLOADING (4GB)", c_name, processed, total, batch_start_time, uid, task_type]

                for mtype, func in send_funcs.items():
                    if f.endswith('.mp4'): mtype = 'video'
                    if getattr(m, mtype, None):
                        sent = await func(LOG_GROUP, f, thumb=th if mtype == 'video' else None, 
                                        duration=dur if mtype == 'video' else None,
                                        height=h if mtype == 'video' else None,
                                        width=w if mtype == 'video' else None,
                                        caption=ft if m.caption and mtype not in ['video_note', 'voice'] else None, 
                                        reply_to_message_id=rtmid, progress=progress_bar, progress_args=p_args)
                        break
                else:
                    sent = await Y.send_document(LOG_GROUP, f, thumb=th, caption=ft if m.caption else None,
                                                reply_to_message_id=rtmid, progress=progress_bar, progress_args=p_args)
                
                await c.copy_message(d, LOG_GROUP, sent.id)
                os.remove(f)
                # await c.delete_messages(d, p.id)
                
                return 'Done (Large file).'
            
            # await c.edit_message_text(d, p.id, 'Uploading...')
            st = time.time()
            p_args = [c, smsg, time.time(), "UPLOADING", c_name, processed, total, batch_start_time, uid, task_type]

            try:
                video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.ogv']
                audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff', '.ac3']
                file_ext = os.path.splitext(f)[1].lower()
                if m.video or (m.document and file_ext in video_extensions):
                    mtd = await get_video_metadata(f)
                    dur, h, w = mtd['duration'], mtd['width'], mtd['height']
                    th = await screenshot(f, dur, d)
                    await c.send_video(tcid, video=f, caption=ft if m.caption else None, 
                                    thumb=th, width=w, height=h, duration=dur, 
                                    progress=progress_bar, progress_args=p_args, 
                                    reply_to_message_id=rtmid)
                elif m.video_note:
                    await c.send_video_note(tcid, video_note=f, progress=progress_bar, 
                                        progress_args=p_args, reply_to_message_id=rtmid)
                elif m.voice:
                    await c.send_voice(tcid, f, progress=progress_bar, progress_args=p_args, 
                                    reply_to_message_id=rtmid)
                elif m.sticker:
                    await c.send_sticker(tcid, m.sticker.file_id, reply_to_message_id=rtmid)
                elif m.audio or (m.document and file_ext in audio_extensions):
                    await c.send_audio(tcid, audio=f, caption=ft if m.caption else None, 
                                    thumb=th, progress=progress_bar, progress_args=p_args, 
                                    reply_to_message_id=rtmid)
                elif m.photo:
                    await c.send_photo(tcid, photo=f, caption=ft if m.caption else None, 
                                    progress=progress_bar, progress_args=p_args, 
                                    reply_to_message_id=rtmid)
                elif m.document:
                    await c.send_document(tcid, document=f, caption=ft if m.caption else None, 
                                        progress=progress_bar, progress_args=p_args, 
                                        reply_to_message_id=rtmid)
                else:
                    await c.send_document(tcid, document=f, caption=ft if m.caption else None, 
                                        progress=progress_bar, progress_args=p_args, 
                                        reply_to_message_id=rtmid)
            except Exception as e:
                # await c.edit_message_text(d, p.id, f'Upload failed: {str(e)[:30]}')
                if os.path.exists(f): os.remove(f)
                return 'Failed.'
            
            os.remove(f)
            # await c.delete_messages(d, p.id)
            
            return 'Done.'
            
        elif m.text:
            await c.send_message(tcid, text=m.text.markdown, reply_to_message_id=rtmid)
            return 'Sent.'
    except Exception as e:
        return f'Error: {str(e)[:50]}'
        
@X.on_message(filters.command(['batch', 'single']))
async def process_cmd(c, m):
    uid = m.from_user.id
    cmd = m.command[0]
    
    if FREEMIUM_LIMIT == 0 and not await is_premium_user(uid):
        await m.reply_text("This bot does not provide free servies, get subscription from OWNER")
        return
    
    if await sub(c, m) == 1: return
    pro = await m.reply_text('Doing some checks hold on...')
    
    if is_user_active(uid):
        await pro.edit('You have an active task. Use /stop to cancel it.')
        return
    
    ubot = await get_ubot(uid)
    if not ubot:
        await pro.edit('Add your bot with /setbot first')
        return
    
    Z[uid] = {'step': 'start' if cmd == 'batch' else 'start_single'}
    await pro.edit(f'Send {"start link..." if cmd == "batch" else "link you to process"}.')

@X.on_message(filters.command(['cancel', 'stop']))
async def cancel_cmd(c, m):
    uid = m.from_user.id
    if is_user_active(uid):
        if await request_batch_cancel(uid):
            await m.reply_text('Cancellation requested. The current batch will stop after the current download completes.')
        else:
            await m.reply_text('Failed to request cancellation. Please try again.')
    else:
        await m.reply_text('No active batch process found.')

@X.on_message(filters.text & filters.private & ~login_in_progress & ~filters.command([
    'start', 'batch', 'cancel', 'login', 'logout', 'stop', 'set', 
    'pay', 'redeem', 'gencode', 'single', 'generate', 'keyinfo', 'encrypt', 'decrypt', 'keys', 'setbot', 'rembot']))
async def text_handler(c, m):
    uid = m.from_user.id
    if uid not in Z: return
    s = Z[uid].get('step')
    x = await get_ubot(uid)
    if not x:
        await message.reply("Add your bot /setbot `token`")
        return

    if s == 'start':
        L = m.text
        i, d, lt = E(L)
        if not i or not d:
            await m.reply_text('Invalid link format.')
            Z.pop(uid, None)
            return
        Z[uid].update({'step': 'count', 'cid': i, 'sid': d, 'lt': lt})
        await m.reply_text('How many messages?')

    elif s == 'start_single':
        L = m.text
        i, d, lt = E(L)
        if not i or not d:
            await m.reply_text('Invalid link format.')
            Z.pop(uid, None)
            return

        Z[uid].update({'step': 'process_single', 'cid': i, 'sid': d, 'lt': lt})
        i, s, lt = Z[uid]['cid'], Z[uid]['sid'], Z[uid]['lt']
        # pt = await m.reply_text('Processing...')
        
        ubot = UB.get(uid)
        if not ubot:
            await m.reply_text('Add bot with /setbot first')
            Z.pop(uid, None)
            return
        
        uc = await get_uclient(uid)
        if not uc:
            await m.reply_text('Cannot proceed without user client.')
            Z.pop(uid, None)
            return
            
        if is_user_active(uid):
            await m.reply_text('Active task exists. Use /stop first.')
            Z.pop(uid, None)
            return

        refresh_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 REFRESH STATUS", callback_data=f"refresh_status_SINGLE")]])
        smsg = await m.reply_text("**🔄 INITIALIZING TASK...**", reply_markup=refresh_btn)
        batch_start_time = time.time()

        try:
            msg = await get_msg(ubot, uc, i, s, lt)
            if msg:
                res = await process_msg(ubot, uc, msg, str(m.chat.id), lt, uid, i, smsg=smsg, batch_start_time=batch_start_time, processed=0, total=1, task_type="SINGLE")
                await smsg.edit(f'1/1: {res}')
            else:
                await smsg.edit('Message not found')
        except Exception as e:
            await smsg.edit(f'Error: {str(e)[:50]}')
        finally:
            Z.pop(uid, None)
            unique_key = f"{uid}_SINGLE"
            if unique_key in batch_temp.PROGRESS_DATA: del batch_temp.PROGRESS_DATA[unique_key]

    elif s == 'count':
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

        # pt = await m.reply_text('Processing batch...')
        uc = await get_uclient(uid)
        ubot = UB.get(uid)
        
        if not uc or not ubot:
            await m.reply_text('Missing client setup')
            Z.pop(uid, None)
            return
            
        if is_user_active(uid):
            await m.reply_text('Active task exists')
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
                
                try:
                    msg = await get_msg(ubot, uc, i, mid, lt)
                    if msg:
                        try: await smsg.edit(f"**🔄 PROCESSING: {j+1}/{n}**", reply_markup=refresh_btn)
                        except: pass
                        res = await process_msg(ubot, uc, msg, str(m.chat.id), lt, uid, i, smsg=smsg, batch_start_time=batch_start_time, processed=j+1, total=n, task_type="BATCH")
                        if 'Done' in res or 'Copied' in res or 'Sent' in res:
                            success += 1
                    else:
                        pass
                except Exception as e:
                    try: await smsg.edit(f'{j+1}/{n}: Error - {str(e)[:30]}')
                    except: pass
                
                await asyncio.sleep(10)
            
            if j+1 == n:
                await m.reply_text(f'Batch Completed ✅ Success: {success}/{n}')
        
        finally:
            await remove_active_batch(uid)
            Z.pop(uid, None)
            unique_key = f"{uid}_BATCH"
            if unique_key in batch_temp.PROGRESS_DATA: del batch_temp.PROGRESS_DATA[unique_key]



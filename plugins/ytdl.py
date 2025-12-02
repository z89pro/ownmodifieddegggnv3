# ---------------------------------------------------
# File Name: ytdl.py
# Description: Fixed Download Logic with Cookies
# ---------------------------------------------------

import yt_dlp
import os
import tempfile
import time
import asyncio
import random
import string
import logging
import aiohttp 
from concurrent.futures import ThreadPoolExecutor

# Import Client & Config
from shared_client import client
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from config import YT_COOKIES, INSTA_COOKIES
from utils.func import fast_upload, progress_callback, get_video_metadata, screenshot
from mutagen.id3 import ID3, TIT2, TPE1, COMM, APIC
from mutagen.mp3 import MP3

logger = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor()
ongoing_downloads = {}

def get_random_string(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length)) 

async def download_thumbnail(url, path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await resp.read())
                    return path
    except Exception as e:
        logger.error(f"Thumbnail download failed: {e}")
    return None

async def extract_info_async(ydl, url, download=True):
    return await asyncio.get_event_loop().run_in_executor(
        thread_pool, 
        lambda: ydl.extract_info(url, download=download)
    )

# ─── AUDIO DOWNLOADER ──────────────────────────────────────────────────────────

async def process_audio(client, event, url, cookies_content=None):
    user_id = event.sender_id
    temp_cookie_path = None
    
    # Create temp cookie file if content exists
    if cookies_content:
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
                f.write(cookies_content)
                temp_cookie_path = f.name
        except Exception as e:
            logger.error(f"Cookie write error: {e}")

    random_id = get_random_string()
    output_template = f"audio_{user_id}_{random_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'cookiefile': temp_cookie_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': False,
        'noplaylist': True,
    }

    msg = await event.reply("🎵 **Downloading Audio...**")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await extract_info_async(ydl, url, download=True)
        
        # Determine filename
        if 'requested_downloads' in info_dict:
            file_path = info_dict['requested_downloads'][0]['filepath']
        else:
            file_path = output_template.replace("%(ext)s", "mp3")

        if not os.path.exists(file_path):
            import glob
            files = glob.glob(f"audio_{user_id}_{random_id}*.mp3")
            if files:
                file_path = files[0]
            else:
                await msg.edit("❌ Download failed: File not found.")
                return

        # Metadata
        title = info_dict.get('title', 'Audio')
        await msg.edit("🏷️ **Adding Metadata...**")
        
        try:
            audio = MP3(file_path, ID3=ID3)
            try:
                audio.add_tags()
            except: 
                pass
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text="Team SPY Bot"))
            audio.save()
        except Exception as e:
            logger.warning(f"Metadata error: {e}")

        # Upload
        await msg.edit("⬆️ **Uploading...**")
        uploaded = await fast_upload(
            client, file_path, 
            reply=msg, 
            progress_bar_function=lambda d, t: progress_callback(d, t, user_id)
        )
        
        await client.send_file(
            event.chat_id, 
            uploaded, 
            caption=f"🎧 **{title}**\n\nby Team SPY"
        )
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ **Error:** `{str(e)[:200]}`")
        logger.error(f"Audio Error: {e}")
    finally:
        if temp_cookie_path and os.path.exists(temp_cookie_path):
            os.remove(temp_cookie_path)
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@client.on(events.NewMessage(pattern="/adl"))
async def audio_handler(event):
    if len(event.message.text.split()) < 2:
        return await event.reply("Usage: `/adl <link>`")
    
    url = event.message.text.split()[1]
    user_id = event.sender_id
    
    if user_id in ongoing_downloads:
        return await event.reply("⚠️ Wait for current task to finish.")
    
    ongoing_downloads[user_id] = True
    try:
        cookies = INSTA_COOKIES if "instagram.com" in url else YT_COOKIES
        await process_audio(client, event, url, cookies)
    finally:
        if user_id in ongoing_downloads:
            del ongoing_downloads[user_id]

# ─── VIDEO DOWNLOADER ──────────────────────────────────────────────────────────

async def process_video(client, event, url, cookies_content=None):
    user_id = event.sender_id
    temp_cookie_path = None
    
    if cookies_content:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
            f.write(cookies_content)
            temp_cookie_path = f.name

    random_id = get_random_string()
    output_template = f"video_{user_id}_{random_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'cookiefile': temp_cookie_path,
        'writethumbnail': True,
        'quiet': False,
    }

    msg = await event.reply("🎥 **Downloading Video...**")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await extract_info_async(ydl, url, download=True)

        # Find file
        file_path = None
        if 'requested_downloads' in info_dict:
            file_path = info_dict['requested_downloads'][0]['filepath']
        
        if not file_path or not os.path.exists(file_path):
            import glob
            files = glob.glob(f"video_{user_id}_{random_id}*")
            video_files = [f for f in files if not f.endswith(('.jpg', '.webp', '.png', '.txt'))]
            if video_files:
                file_path = video_files[0]
            else:
                await msg.edit("❌ Download failed: File not found.")
                return

        # Metadata extraction
        title = info_dict.get('title', 'Video')
        duration = info_dict.get('duration', 0)
        width = info_dict.get('width', 0)
        height = info_dict.get('height', 0)
        
        # Thumbnail
        thumb_path = None
        if info_dict.get('thumbnail'):
            thumb_path = f"thumb_{user_id}_{random_id}.jpg"
            await download_thumbnail(info_dict['thumbnail'], thumb_path)
        
        if not thumb_path:
            thumb_path = await screenshot(file_path, duration, user_id)

        # Upload
        await msg.edit("⬆️ **Uploading...**")
        uploaded = await fast_upload(
            client, file_path,
            reply=msg,
            progress_bar_function=lambda d, t: progress_callback(d, t, user_id)
        )

        await client.send_file(
            event.chat_id,
            uploaded,
            caption=f"🎥 **{title}**",
            thumb=thumb_path,
            attributes=[DocumentAttributeVideo(
                duration=int(duration),
                w=int(width),
                h=int(height),
                supports_streaming=True
            )]
        )
        await msg.delete()

    except Exception as e:
        err_msg = str(e)
        if "Sign in" in err_msg:
            await msg.edit("❌ **Cookie Error:** YouTube requires login. Cookies might be expired.")
        else:
            await msg.edit(f"❌ **Error:** `{err_msg[:200]}`")
        logger.error(f"Video Error: {e}")
    finally:
        # Cleanup
        if temp_cookie_path and os.path.exists(temp_cookie_path):
            os.remove(temp_cookie_path)
        if 'file_path' in locals() and file_path and os.path.exists(file_path):
            os.remove(file_path)
        if 'thumb_path' in locals() and thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

@client.on(events.NewMessage(pattern="/dl"))
async def video_handler(event):
    if len(event.message.text.split()) < 2:
        return await event.reply("Usage: `/dl <link>`")
    
    url = event.message.text.split()[1]
    user_id = event.sender_id
    
    if user_id in ongoing_downloads:
        return await event.reply("⚠️ Wait for current task to finish.")
    
    ongoing_downloads[user_id] = True
    try:
        cookies = INSTA_COOKIES if "instagram.com" in url else YT_COOKIES
        await process_video(client, event, url, cookies)
    finally:
        if user_id in ongoing_downloads:
            del ongoing_downloads[user_id]

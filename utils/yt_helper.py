"""
Enhanced YT-DLP Download Helper with Browser Cookie Support
Author: Gagan (Enhanced by Master Coder for Anti-Bot Evasion)
Features:
- Fixed User-Agent Mismatch (Android Client Enforcement)
- Browser cookie auto-extraction
- Retry logic with exponential backoff
- Rate limit prevention
"""

import yt_dlp
from yt_dlp.utils import sanitize_filename, DownloadError
import os
import time
import asyncio
import tempfile
import logging
import subprocess
from typing import Optional, Dict, Any
from telethon import events, Button
from shared_client import client
from shared_client import app  # Pyrogram app
from config import YT_COOKIES, INSTA_COOKIES
# Agar config mein proxy hai toh wahan se import karo, warna None
try:
    from config import HTTP_PROXY
except ImportError:
    HTTP_PROXY = None

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM, APIC
from utils.func import fast_upload, progress_callback, get_video_metadata, screenshot, d_thumbnail, get_random_string
from pyrogram.types import DocumentAttributeVideo
from utils.message_manager import MessageManager

logger = logging.getLogger(__name__)
ongoing_downloads = {}
pending_selection = {}

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
DOWNLOAD_DELAY = 2  # seconds between downloads

class CookieManager:
    """Manages cookie extraction and handling"""
    
    @staticmethod
    def try_browser_cookies(url: str) -> Optional[str]:
        """
        Try to extract cookies from browser
        Returns: browser name if successful, None otherwise
        """
        browsers = ['chrome', 'firefox', 'edge', 'brave']
        
        for browser in browsers:
            try:
                # Test if yt-dlp can extract cookies
                opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'cookiesfrombrowser': (browser,),
                }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.extract_info(url, download=False)
                logger.info(f"Successfully extracted cookies from {browser}")
                return browser
            except Exception:
                continue
        return None
    
    @staticmethod
    def create_cookie_file(cookies_text: str) -> Optional[str]:
        """Create temporary cookie file from text"""
        if not cookies_text:
            return None
        
        try:
            # Netscape format check
            if not cookies_text.strip().startswith("# Netscape"):
                 # Agar user ne galti se header nahi lagaya, toh hum laga dete hain
                 cookies_text = "# Netscape HTTP Cookie File\n" + cookies_text

            temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt')
            temp_file.write(cookies_text)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            logger.error(f"Failed to create cookie file: {e}")
            return None

def get_ydl_opts(url: str, cookies_env_var: Optional[str] = None, format_spec: str = 'best') -> Dict[str, Any]:
    """
    Get yt-dlp options with enhanced settings and Anti-Detection
    """
    opts = {
        'quiet': False,
        'no_warnings': False,
        'format': format_spec,
        # 'http_headers' REMOVED: Preventing User-Agent mismatch
        'extractor_args': {
            'youtube': {
                # Forces pure Android API usage which is more lenient on Data Centers
                'player_client': ['android'],
                'skip': ['dash', 'hls'],
            },
            'instagram': {
                'api_version': '1',
            }
        },
        'extractor_retries': 3,
        'fragment_retries': 10,
        'socket_timeout': 30,
    }

    # Add Proxy if available in config
    if HTTP_PROXY:
        opts['proxy'] = HTTP_PROXY
    
    # Cookie Handling
    if "youtube.com" in url or "youtu.be" in url or "instagram.com" in url:
        # 1. Try Browser (Localhost only)
        browser = CookieManager.try_browser_cookies(url)
        if browser:
            opts['cookiesfrombrowser'] = (browser,)
            logger.info(f"Using browser cookies from {browser}")
        # 2. Fallback to ENV/Config Cookies (Server/Cloud)
        elif cookies_env_var:
            cookie_file = CookieManager.create_cookie_file(cookies_env_var)
            if cookie_file:
                opts['cookiefile'] = cookie_file
                logger.info("Using environment cookies")
    
    return opts

async def download_with_retry(url: str, ydl_opts: Dict[str, Any], progress_message, max_retries: int = MAX_RETRIES) -> Optional[Dict]:
    """
    Download with retry logic and exponential backoff
    """
    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = await asyncio.to_thread(ydl.extract_info, url, download=True)
            return info_dict
        except DownloadError as e:
            error_msg = str(e).lower()
            
            # Check for specific error types
            if "sign in" in error_msg or "login" in error_msg:
                await progress_message.edit(
                    "**❌ Authentication Required**\n\n"
                    "YouTube is asking for Login. This usually means:\n"
                    "1. Your Server IP is flagged.\n"
                    "2. Cookies are expired.\n\n"
                    "**Fix:** Update `YT_COOKIES` with fresh exported cookies."
                )
                return None
            elif "rate" in error_msg or "too many requests" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    await progress_message.edit(f"**⏳ Rate limited. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...**")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    await progress_message.edit(
                        "**❌ Rate Limit Exceeded**\n\n"
                        f"Failed after {max_retries} attempts.\n"
                        "Server IP is likely blocked for now."
                    )
                    return None
            elif "private" in error_msg or "not available" in error_msg:
                await progress_message.edit(
                    "**❌ Content Not Available**\n\n"
                    "This content is private, deleted, or geo-restricted."
                )
                return None
            else:
                # Generic error with retry
                if attempt < max_retries - 1:
                    await progress_message.edit(f"**⚠️ Error occurred. Retrying {attempt + 2}/{max_retries}...**")
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                else:
                    await progress_message.edit(f"**❌ Download Failed**\n\n`{str(e)[:200]}`")
                    return None
        except Exception as e:
            logger.exception("Unexpected error during download")
            await progress_message.edit(f"**❌ Unexpected Error**\n\n`{str(e)[:200]}`")
            return None
    
    return None

async def extract_audio_async(ydl_opts: Dict[str, Any], url: str) -> Dict:
    """Extract audio asynchronously"""
    def extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url,download=True)
    return await asyncio.to_thread(extract)

async def download_thumbnail_async(url: str, path: str):
    """Download thumbnail asynchronously"""
    def download():
        import requests
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            logger.error(f"Thumbnail download failed: {e}")
            
    await asyncio.to_thread(download)

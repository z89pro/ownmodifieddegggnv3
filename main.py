# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os
import sys
import glob
import logging

# Global variables to store client instances
client = None
app = None
userbot = None

def cleanup_temp_files():
    """Delete all temporary and corrupted files on startup"""
    print("Cleaning up temporary files...")
    try:
        patterns = ['*.mp3', '*.mp4', '*.mkv', '*.jpg', '*.png', '*.webm', '*.part', '*.ytdl', '*.temp']
        deleted_count = 0
        
        for pattern in patterns:
            for file in glob.glob(pattern):
                try:
                    os.remove(file)
                    deleted_count += 1
                except Exception as e:
                    print(f"Could not delete {file}: {e}")
        
        if deleted_count > 0:
            print(f"Cleaned up {deleted_count} temporary files")
    except Exception as e:
        print(f"Error during cleanup: {e}")

async def load_and_run_plugins():
    global client, app, userbot
    # Run cleanup before starting clients
    cleanup_temp_files()
    
    # Capture the returned client instances
    client, app, userbot = await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()  

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Critical error in main loop: {e}")
        sys.stdout.flush()
        sys.exit(1)
    finally:
        try:
            if not loop.is_closed():
                loop.close()
        except Exception:
            pass
        sys.stdout.flush()

# ... (Imports remain the same)
from config import YT_COOKIES, INSTA_COOKIES # Ensure these are imported
# ... 

# ... (Previous code remains)

@client.on(events.NewMessage(pattern="/adl"))
async def handler(event):
    user_id = event.sender_id
    if user_id in ongoing_downloads:
        await event.reply("**You already have an ongoing download. Please wait!**")
        return
 
    if len(event.message.text.split()) < 2:
        await event.reply("**Usage:** `/adl <video-link>`")
        return    
 
    url = event.message.text.split()[1]
    ongoing_downloads[user_id] = True
 
    try:
        # FIX: Passing the actual variable, NOT the string name
        if "instagram.com" in url:
            await process_audio(client, event, url, cookies_env_var=INSTA_COOKIES)
        elif "youtube.com" in url or "youtu.be" in url:
            await process_audio(client, event, url, cookies_env_var=YT_COOKIES)
        else:
            await process_audio(client, event, url)
    except Exception as e:
        await event.reply(f"**An error occurred:** `{e}`")
    finally:
        ongoing_downloads.pop(user_id, None)

# ... (Middle code remains)

@client.on(events.NewMessage(pattern="/dl"))
async def handler(event):
    user_id = event.sender_id
    if user_id in ongoing_downloads:
        await event.reply("**Wait for current download to finish!**")
        return
 
    if len(event.message.text.split()) < 2:
        await event.reply("**Usage:** `/dl <video-link>`")
        return    
 
    url = event.message.text.split()[1]
    ongoing_downloads[user_id] = True

    try:
        # FIX: Passing the actual variable, NOT the string name
        if "instagram.com" in url:
            await process_video(client, event, url, INSTA_COOKIES, check_duration_and_size=False)
        elif "youtube.com" in url or "youtu.be" in url:
            await process_video(client, event, url, YT_COOKIES, check_duration_and_size=True)
        else:
            await process_video(client, event, url, None, check_duration_and_size=False)
 
    except Exception as e:
        await event.reply(f"**An error occurred:** `{e}`")
    finally:
        ongoing_downloads.pop(user_id, None)

# ... (Rest of the file remains)

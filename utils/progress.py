import time
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class batch_temp(object):
    IS_BATCH = {}
    BATCH_TASKS = {}
    SINGLE_TASKS = {}
    PROGRESS_DATA = {} 

def humanbytes(size):
    if not size: return "0 B"
    power = 2**10
    n = 0
    dic_powerN = {0: ' ', 1: 'KiB', 2: 'MiB', 3: 'GiB', 4: 'TiB'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {dic_powerN[n]}"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((f"{days}d " if days else "") + (f"{hours}h " if hours else "") + (f"{minutes}m " if minutes else "") + (f"{seconds}s" if seconds else ""))
    if not tmp: return "0s"
    return tmp

async def progress_bar(current, total, client, message, start, type, file_name, processed_msgs, total_msgs, batch_start_time, user_id, task_type):
    # 🚨 KILL SWITCH: This stops download instantly
    if task_type == "BATCH" and batch_temp.BATCH_TASKS.get(user_id):
        raise Exception("FORCE_CANCEL")
    if task_type == "SINGLE" and batch_temp.SINGLE_TASKS.get(user_id):
        raise Exception("FORCE_CANCEL")

    now = time.time()
    diff = now - start
    
    percentage = (current * 100) / total if total > 0 else 0
    speed = current / diff if diff > 0 else 0
    eta = round((total - current) / speed) if speed > 0 else 0
    
    unique_key = f"{user_id}_{task_type}"
    
    batch_temp.PROGRESS_DATA[unique_key] = {
        "current": current,
        "total": total,
        "percentage": percentage,
        "speed": speed,
        "eta": eta,
        "type": type,
        "file_name": file_name,
        "processed": processed_msgs,
        "total_msgs": total_msgs,
        "batch_start": batch_start_time,
        "task_type": task_type
    }

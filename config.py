# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.

import os
from dotenv import load_dotenv
load_dotenv()

# ════════════════════════════════════════════════════════════════════════════════
# ░ CONFIGURATION SETTINGS
# ════════════════════════════════════════════════════════════════════════════════

# 1. Instagram Cookies (Variable name fixed to INSTA_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", "")

# 2. YouTube Cookies
YT_COOKIES = os.getenv("YT_COOKIES", "")

# ─── BOT / DATABASE CONFIG ──────────────────────────────────────────────────────
# Safe conversion to prevent Import Crashes
try:
    API_ID = int(os.getenv("API_ID", "0"))
except ValueError:
    print("⚠️ API_ID INVALID! Must be an integer.")
    API_ID = 27298762

API_HASH     = os.getenv("API_HASH", "ed1afeb86effb107b287d5d3aeaefe4a")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "8428805859:AAFlf5Rqvu-fCoqOy5dhoUh5QZQk9K78RiI")
MONGO_DB     = os.getenv("MONGO_DB", "mongodb+srv://defet54636_db_user:XmIjdhGyimZuak59@cluster0.xepvgb3.mongodb.net/?appName=Cluster0")
DB_NAME      = os.getenv("DB_NAME", "telegram_downloader")

# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
owner_id_str = os.getenv("OWNER_ID", "")
OWNER_ID     = list(map(int, owner_id_str.split())) if owner_id_str else []

STRING       = os.getenv("STRING", None)
LOG_GROUP    = int(os.getenv("LOG_GROUP", "-1004426994491"))
FORCE_SUB    = int(os.getenv("FORCE_SUB", "-1004428543058"))

# ─── SECURITY KEYS ──────────────────────────────────────────────────────────────
MASTER_KEY   = os.getenv("MASTER_KEY", "QWeCQl7F91DPGUdimsgic7_KwAKSx-NgQ8CAVBWaac8=")
IV_KEY       = os.getenv("IV_KEY", "HOl_k8Dypv6cG_6nIyYbxg==")

# ─── USAGE LIMITS ───────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "10000"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "50000000"))

# ─── UI / LINKS ─────────────────────────────────────────────────────────────────
JOIN_LINK     = os.getenv("JOIN_LINK", "https://t.me/+ATllYz3gW01lYzM9")
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/username_of_admin")

# Proxy Support
HTTP_PROXY = os.getenv("HTTP_PROXY", None)

# ════════════════════════════════════════════════════════════════════════════════
# ░ PREMIUM PLANS CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════════

P0 = {
    "d": {
        "s": int(os.getenv("PLAN_D_S", 1)),
        "du": int(os.getenv("PLAN_D_DU", 1)),
        "u": os.getenv("PLAN_D_U", "days"),
        "l": os.getenv("PLAN_D_L", "Daily"),
    },
    "w": {
        "s": int(os.getenv("PLAN_W_S", 3)),
        "du": int(os.getenv("PLAN_W_DU", 1)),
        "u": os.getenv("PLAN_W_U", "weeks"),
        "l": os.getenv("PLAN_W_L", "Weekly"),
    },
    "m": {
        "s": int(os.getenv("PLAN_M_S", 5)),
        "du": int(os.getenv("PLAN_M_DU", 1)),
        "u": os.getenv("PLAN_M_U", "month"),
        "l": os.getenv("PLAN_M_L", "Monthly"),
    },
}

# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import os
from dotenv import load_dotenv
load_dotenv()

# ════════════════════════════════════════════════════════════════════════════════
# ░ CONFIGURATION SETTINGS
# ════════════════════════════════════════════════════════════════════════════════

# VPS --- FILL COOKIES 🍪 in """ ... """ 

# 1. Instagram Cookies
INST_COOKIES = """
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	TRUE	1798556010	datr	anEkaXKfPtG0mP9ORmeTO6H5
.instagram.com	TRUE	/	TRUE	1795532391	ig_did	E8BBB57D-D97D-48BC-A9CD-9061560931C8
.instagram.com	TRUE	/	TRUE	1765198008	wd	1366x641
.instagram.com	TRUE	/	TRUE	1795532064	ig_nrcb	1
.instagram.com	TRUE	/	TRUE	1772369218	ds_user_id
"""

# 2. YouTube Cookies
YTUB_COOKIES = """
# Netscape HTTP Cookie File
.google.com	TRUE	/verify	TRUE	1780402771	SNID	AICKk4wG6wrAwCHJAumEOvM8VoBm-rg9JH_Y43C6aDSeb8kG7Z4Cgt9ftDvzLJU2vPMb-w3bbPjrq6i3fmFXmH-QPSPMop_Qeg
.google.com	TRUE	/	TRUE	1780143572	AEC	AaJma5s4jg3mg2Uaqfmz6h6Cg0OHBbdLiQ-asRV2ZLBm7Fl6gOhWqwYs-tw
.google.com	TRUE	/	TRUE	1780402771	NID	526=kqEAcjHTmsGphhk2K7Uz4wiCKqIv7wX-8kWTyssni6egyGBMbSpsEWZ-wLltCVyXEkRUxprY4Z0mPhI6JGw8OLK_meqU4xJLjDmApQ5ZD2sxB3PQsTmFNjrRCfcCTV54uLq-1ycEXwZldT__PvxOtkCRP26RqBvlw620Q4PEzuHYqE2wiJnaf9DbKFDxfOTgFeZv3wpNwFDRbydjY4ZCUL-pasa0huXXR9_wQ7zQYCGM79VCapd7m0KzppOO-CqB9-o
.youtube.com	TRUE	/	TRUE	1764593374	GPS	1
.youtube.com	TRUE	/	TRUE	1799151578	PREF	tz=Asia.Calcutta
.youtube.com	TRUE	/	TRUE	0	YSC	nAa3uvsZPxU
.youtube.com	TRUE	/	TRUE	1780143579	VISITOR_INFO1_LIVE	W7NJqAXQrYY
.youtube.com	TRUE	/	TRUE	1780143579	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgUw%3D%3D
.youtube.com	TRUE	/	TRUE	1780143577	__Secure-ROLLOUT_TOKEN	CKHQn7jRrtXMzAEQ8fKf76-ckQMY1_Ta8K-ckQM%3D
"""

# ─── BOT / DATABASE CONFIG ──────────────────────────────────────────────────────
API_ID       = os.getenv("API_ID", "")
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
MONGO_DB     = os.getenv("MONGO_DB", "")
DB_NAME      = os.getenv("DB_NAME", "telegram_downloader")

# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
# Use .get with a fallback to avoid errors if OWNER_ID is not set in env
owner_id_str = os.getenv("OWNER_ID", "8349955493")
OWNER_ID     = list(map(int, owner_id_str.split())) if owner_id_str else []

STRING       = os.getenv("STRING", None)
LOG_GROUP    = int(os.getenv("LOG_GROUP", "-1001234456"))
FORCE_SUB    = int(os.getenv("FORCE_SUB", "-10012345567"))

# ─── SECURITY KEYS ──────────────────────────────────────────────────────────────
MASTER_KEY   = os.getenv("MASTER_KEY", "QWeCQl7F91DPGUdimsgic7_KwAKSx-NgQ8CAVBWaac8=")
IV_KEY       = os.getenv("IV_KEY", "HOl_k8Dypv6cG_6nIyYbxg==")

# ─── COOKIES HANDLING ───────────────────────────────────────────────────────────
# Priorities: Env Variable > Config File Hardcode
YT_COOKIES   = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)

# ─── USAGE LIMITS ───────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "500"))

# ─── UI / LINKS ─────────────────────────────────────────────────────────────────
JOIN_LINK     = os.getenv("JOIN_LINK", "https://t.me/team_spy_pro")
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/username_of_admin")

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


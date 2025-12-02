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
INST_COOKIES = """
# write up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

# ─── BOT / DATABASE CONFIG ──────────────────────────────────────────────────────
API_ID       = os.getenv("API_ID", "")
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
MONGO_DB     = os.getenv("MONGO_DB", "")
DB_NAME      = os.getenv("DB_NAME", "telegram_downloader")

# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
OWNER_ID     = list(map(int, os.getenv("OWNER_ID", "8349955493").split()))  # space-separated list
STRING       = os.getenv("STRING", None)  # optional session string
LOG_GROUP    = int(os.getenv("LOG_GROUP", "-1001234456"))
FORCE_SUB    = int(os.getenv("FORCE_SUB", "-10012345567"))

# ─── SECURITY KEYS ──────────────────────────────────────────────────────────────
MASTER_KEY   = os.getenv("MASTER_KEY", "QWeCQl7F91DPGUdimsgic7_KwAKSx-NgQ8CAVBWaac8=")  # session encryption
IV_KEY       = os.getenv("IV_KEY", "HOl_k8Dypv6cG_6nIyYbxg==")  # decryption key

# ─── COOKIES HANDLING ───────────────────────────────────────────────────────────
YT_COOKIES   = os.getenv("# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	FALSE	1799075831	HSID	A-zujUGStEyVxZ4DE
.youtube.com	TRUE	/	TRUE	1799075831	SSID	ACsQjqpP3nkQhr5_O
.youtube.com	TRUE	/	FALSE	1799075831	APISID	AEg4G0DDkwxJDbMw/ADiEP_2ySTk-h0oT0
.youtube.com	TRUE	/	TRUE	1799075831	SAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-1PAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-3PAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799226663	PREF	tz=Asia.Calcutta&f7=100&f5=30000
.youtube.com	TRUE	/	FALSE	1799075831	SID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQsXV8Up84J2MZpcSOupBqOwACgYKAQgSARcSFQHGX2Mi5OmCvd30Y3R12VOwaDDf-xoVAUF8yKoqrCyVJV3fDNd6yTYvlehM0076
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-1PSID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQ5dJAjSItccPNl5CK9cKlmAACgYKAZYSARcSFQHGX2Mie91mTJwR6EesuDwYkvgD1RoVAUF8yKpEPbiV39Pxi2n7-vBCrr6-0076
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-3PSID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQRJdv2XtsiW80TVMiRLOGEwACgYKAb4SARcSFQHGX2MihX5qnnzAuAQIE2BgB1C6VRoVAUF8yKr2bYX4bbb0qxbxIyJLnLSn0076
.youtube.com	TRUE	/	FALSE	0	wide	0
.youtube.com	TRUE	/	TRUE	1799164670	LOGIN_INFO	AFmmF2swRQIhAMxPINDnqsGGsEeK5oQMMjevQ9vJv7N0qgvXMZCE5pbmAiAZPUzpKMnAY_aD18bQHF_m8CUJZcmuVjDFqcTHhzDnoA:QUQ3MjNmenk1RkstOE1FNjMxQUczb2FpWS1Wc2Y2c005UHRPVGc2d0wxR2tJTUhxdTdfTnhOZWJPS2ZVSkhMWW9Hc3Y2OE1IaDB1TTBlUGFnRWtUTVlhSkpuQTBBQmNsMzEzYkFzT04zamcxZFRNdHotZU9WU2lBODdzU3BoOFJPd09pdVk2bTBmMng3ZlNsZjlsMVdObndXcUJpckZoS004R09Gb1pBNW9tZEhsaHJ0bmZsa1luRkx1UWVDYTF2MXY4UklSd1NVOTVIeXNsaDl1bVhtTVJLeVA5dm1FVmV3UQ==
.youtube.com	TRUE	/	TRUE	1764666761	CONSISTENCY	AKreu9sI5zSza1RBsH39_-KVj77Hmed0KLlmwNp2lDc8XU8KUs0nXSU2zVRqVVWf375tIXZ0o8qbUrWnTF31cSSsR65i4-amwJgiamwT6PKAQY-a_twTsFzZXrI
.youtube.com	TRUE	/	FALSE	1764666673	ST-3opvp5	session_logininfo=AFmmF2swRQIhAMxPINDnqsGGsEeK5oQMMjevQ9vJv7N0qgvXMZCE5pbmAiAZPUzpKMnAY_aD18bQHF_m8CUJZcmuVjDFqcTHhzDnoA%3AQUQ3MjNmenk1RkstOE1FNjMxQUczb2FpWS1Wc2Y2c005UHRPVGc2d0wxR2tJTUhxdTdfTnhOZWJPS2ZVSkhMWW9Hc3Y2OE1IaDB1TTBlUGFnRWtUTVlhSkpuQTBBQmNsMzEzYkFzT04zamcxZFRNdHotZU9WU2lBODdzU3BoOFJPd09pdVk2bTBmMng3ZlNsZjlsMVdObndXcUJpckZoS004R09Gb1pBNW9tZEhsaHJ0bmZsa1luRkx1UWVDYTF2MXY4UklSd1NVOTVIeXNsaDl1bVhtTVJLeVA5dm1FVmV3UQ%3D%3D
.youtube.com	TRUE	/	TRUE	1796202668	__Secure-1PSIDTS	sidts-CjUBwQ9iI4vFtPKHn9YoxbO_x13DiwrdnIFAFo72RCAYQphq-hSOtElkB9MrU7LdoIARgNGsRBAA
.youtube.com	TRUE	/	TRUE	1796202668	__Secure-3PSIDTS	sidts-CjUBwQ9iI4vFtPKHn9YoxbO_x13DiwrdnIFAFo72RCAYQphq-hSOtElkB9MrU7LdoIARgNGsRBAA
.youtube.com	TRUE	/	FALSE	1796202668	SIDCC	AKEyXzUV15wnQhynxtBoXbXgfDJrbCNrevhDKPamAj_3kso92-ubQflex8UdozY9uZxpMLZ-Bg
.youtube.com	TRUE	/	TRUE	1796202668	__Secure-1PSIDCC	AKEyXzWy4LHrKFF7QEkwhsiXFH3-TMGtmsydLuyvvLw-PPasl6AhQBZjBDXkr_W5a6BxLNQPNw
.youtube.com	TRUE	/	TRUE	1796202668	__Secure-3PSIDCC	AKEyXzU9pru6D1o7arBpFicNXA7XXyeBnm3MzqXbOrLJx5nkkYDhGIQft9FSM7fsKLQRo3OclkU
.youtube.com	TRUE	/	TRUE	0	YSC	hzsa1B54T9g
.youtube.com	TRUE	/	TRUE	1780218658	VISITOR_INFO1_LIVE	mI5miys20K8
.youtube.com	TRUE	/	TRUE	1780218658	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgIg%3D%3D
.youtube.com	TRUE	/	TRUE	1780143474	__Secure-ROLLOUT_TOKEN	CJnm7tjPwLq7WBCVr8qA2oCQAxjf97C_r5yRAw%3D%3D
", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.instagram.com	TRUE	/	TRUE	1799226617	csrftoken	blhdwgPAlFBw76vmFaeq0v
.instagram.com	TRUE	/	TRUE	1799226211	datr	YqsuaRzv-uxcYEwaB9Irfyf1
.instagram.com	TRUE	/	TRUE	1796202231	ig_did	E61F23DA-2CFA-4A65-8B39-366987332FFA
.instagram.com	TRUE	/	TRUE	1765271035	wd	1366x641
.instagram.com	TRUE	/	TRUE	1799226213	mid	aS6rYgALAAENTbhI4-qjC4ejrWTd
.instagram.com	TRUE	/	TRUE	1796202222	ig_nrcb	1
.instagram.com	TRUE	/	TRUE	1796202231	sessionid	71212741072%3ArwfEFg5nbcjUoI%3A22%3AAYhRczhSfC9P5C0Q55l1YsjdF7yyjE3QrrsZKYAc4A
.instagram.com	TRUE	/	TRUE	1772442617	ds_user_id	71212741072
.instagram.com	TRUE	/	TRUE	0	rur	"VLL\05471212741072\0541796202616:01fe4b6ea51587e7ccffd6111ca93bddab7155477ebeaae3f6a4d182a17a2c72de13da31"
", INST_COOKIES)

# ─── USAGE LIMITS ───────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "500"))

# ─── UI / LINKS ─────────────────────────────────────────────────────────────────
JOIN_LINK     = os.getenv("JOIN_LINK", "https://t.me/team_spy_pro")
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "@Zain_0369")

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

# ─── DOWNLOAD SETTINGS ──────────────────────────────────────────────────────────
DOWNLOAD_DELAY = int(os.getenv("DOWNLOAD_DELAY", "2"))  # Seconds between downloads to avoid rate limits
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))  # Number of retry attempts for failed downloads
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))  # Base delay between retries (exponential backoff)

# ─── MESSAGE CLEANUP SETTINGS ───────────────────────────────────────────────────
AUTO_DELETE_COMMANDS = os.getenv("AUTO_DELETE_COMMANDS", "True").lower() == "true"
COMMAND_DELETE_DELAY = int(os.getenv("COMMAND_DELETE_DELAY", "4"))  # Seconds before deleting commands
STATUS_DELETE_DELAY = int(os.getenv("STATUS_DELETE_DELAY", "4"))  # Seconds before deleting status messages
ERROR_DELETE_DELAY = int(os.getenv("ERROR_DELETE_DELAY", "10"))  # Seconds before deleting error messages

# ─── COOKIE SETTINGS (ENHANCED) ─────────────────────────────────────────────────
USE_BROWSER_COOKIES = os.getenv("USE_BROWSER_COOKIES", "True").lower() == "true"  # Try browser cookies first
COOKIE_BROWSER = os.getenv("COOKIE_BROWSER", "chrome")  # chrome, firefox, edge, brave

# ════════════════════════════════════════════════════════════════════════════════
# ░ ERROR MESSAGE (for backward compatibility)
# ════════════════════════════════════════════════════════════════════════════════
ERROR_MESSAGE = "**❌ Error occurred**\\n\\nPlease try again or contact support."

# ════════════════════════════════════════════════════════════════════════════════
# ░ DEVGAGAN
# ════════════════════════════════════════════════════════════════════════════════


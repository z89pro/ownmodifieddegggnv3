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

# 1. Instagram Cookies (Updated from your input)
INST_COOKIES = """
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.instagram.com	TRUE	/	TRUE	1799228949	csrftoken	R5Ujr7dyWa4SnqhGsgCq2J
.instagram.com	TRUE	/	TRUE	1799228934	datr	BbYuaXOsfu_Egxc8OxYkYDoH
.instagram.com	TRUE	/	TRUE	1796204945	ig_did	03087885-A0D6-4E2A-803B-09B965FE824F
.instagram.com	TRUE	/	TRUE	1765273749	wd	1366x641
.instagram.com	TRUE	/	TRUE	1799228936	mid	aS62BQALAAHmidI1p_xJ_72b5ca8
.instagram.com	TRUE	/	TRUE	1796204945	sessionid	71212741072%3AoqtL5KeMgMoz61%3A1%3AAYgbzxoXj2HaFKoli18cQ0D_Fa5BN973K_NVifFNLw
.instagram.com	TRUE	/	TRUE	1772444949	ds_user_id	71212741072
.instagram.com	TRUE	/	TRUE	0	rur	"VLL\\05471212741072\\0541796204948:01feef85623e6f3557bf30a8acc5b92ea04fbd13b2797df3f275201168921a2ca2a6cc83"
"""

# 2. YouTube Cookies (Updated from your input)
YTUB_COOKIES = """
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	FALSE	1799075831	HSID	A-zujUGStEyVxZ4DE
.youtube.com	TRUE	/	TRUE	1799075831	SSID	ACsQjqpP3nkQhr5_O
.youtube.com	TRUE	/	FALSE	1799075831	APISID	AEg4G0DDkwxJDbMw/ADiEP_2ySTk-h0oT0
.youtube.com	TRUE	/	TRUE	1799075831	SAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-1PAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-3PAPISID	xkljk55EJQTXq6MU/AQnIy5tGe_UkugLLk
.youtube.com	TRUE	/	TRUE	1799228904	PREF	tz=Asia.Calcutta&f7=100&f5=30000
.youtube.com	TRUE	/	FALSE	1799075831	SID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQsXV8Up84J2MZpcSOupBqOwACgYKAQgSARcSFQHGX2Mi5OmCvd30Y3R12VOwaDDf-xoVAUF8yKoqrCyVJV3fDNd6yTYvlehM0076
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-1PSID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQ5dJAjSItccPNl5CK9cKlmAACgYKAZYSARcSFQHGX2Mie91mTJwR6EesuDwYkvgD1RoVAUF8yKpEPbiV39Pxi2n7-vBCrr6-0076
.youtube.com	TRUE	/	TRUE	1799075831	__Secure-3PSID	g.a0004AhLwKz9mkwmc5tN4-ruKdSpBCFQeHgS0jQlp5ndiloNfKtQRJdv2XtsiW80TVMiRLOGEwACgYKAb4SARcSFQHGX2MihX5qnnzAuAQIE2BgB1C6VRoVAUF8yKr2bYX4bbb0qxbxIyJLnLSn0076
.youtube.com	TRUE	/	FALSE	0	wide	0
.youtube.com	TRUE	/	TRUE	1799164670	LOGIN_INFO	AFmmF2swRQIhAMxPINDnqsGGsEeK5oQMMjevQ9vJv7N0qgvXMZCE5pbmAiAZPUzpKMnAY_aD18bQHF_m8CUJZcmuVjDFqcTHhzDnoA:QUQ3MjNmenk1RkstOE1FNjMxQUczb2FpWS1Wc2Y2c005UHRPVGc2d0wxR2tJTUhxdTdfTnhOZWJPS2ZVSkhMWW9Hc3Y2OE1IaDB1TTBlUGFnRWtUTVlhSkpuQTBBQmNsMzEzYkFzT04zamcxZFRNdHotZU9WU2lBODdzU3BoOFJPd09pdVk2bTBmMng3ZlNsZjlsMVdObndXcUJpckZoS004R09Gb1pBNW9tZEhsaHJ0bmZsa1luRkx1UWVDYTF2MXY4UklSd1NVOTVIeXNsaDl1bVhtTVJLeVA5dm1FVmV3UQ==
.youtube.com	TRUE	/	FALSE	1764668909	ST-xuwub9	session_logininfo=AFmmF2swRQIhAMxPINDnqsGGsEeK5oQMMjevQ9vJv7N0qgvXMZCE5pbmAiAZPUzpKMnAY_aD18bQHF_m8CUJZcmuVjDFqcTHhzDnoA%3AQUQ3MjNmenk1RkstOE1FNjMxQUczb2FpWS1Wc2Y2c005UHRPVGc2d0wxR2tJTUhxdTdfTnhOZWJPS2ZVSkhMWW9Hc3Y2OE1IaDB1TTBlUGFnRWtUTVlhSkpuQTBBQmNsMzEzYkFzT04zamcxZFRNdHotZU9WU2lBODdzU3BoOFJPd09pdVk2bTBmMng3ZlNsZjlsMVdObndXcUJpckZoS004R09Gb1pBNW9tZEhsaHJ0bmZsa1luRkx1UWVDYTF2MXY4UklSd1NVOTVIeXNsaDl1bVhtTVJLeVA5dm1FVmV3UQ%3D%3D
.youtube.com	TRUE	/	FALSE	1764668912	ST-3opvp5	session_logininfo=AFmmF2swRQIhAMxPINDnqsGGsEeK5oQMMjevQ9vJv7N0qgvXMZCE5pbmAiAZPUzpKMnAY_aD18bQHF_m8CUJZcmuVjDFqcTHhzDnoA%3AQUQ3MjNmenk1RkstOE1FNjMxQUczb2FpWS1Wc2Y2c005UHRPVGc2d0wxR2tJTUhxdTdfTnhOZWJPS2ZVSkhMWW9Hc3Y2OE1IaDB1TTBlUGFnRWtUTVlhSkpuQTBBQmNsMzEzYkFzT04zamcxZFRNdHotZU9WU2lBODdzU3BoOFJPd09pdVk2bTBmMng3ZlNsZjlsMVdObndXcUJpckZoS004R09Gb1pBNW9tZEhsaHJ0bmZsa1luRkx1UWVDYTF2MXY4UklSd1NVOTVIeXNsaDl1bVhtTVJLeVA5dm1FVmV3UQ%3D%3D
.youtube.com	TRUE	/	TRUE	1796204908	__Secure-1PSIDTS	sidts-CjUBwQ9iIyzKnRhKFHwrOzVLhM8fMlFMSAehDL7CCOQAkGKXf0fDIOAaTRu9fYlyPLSRKzqlnhAA
.youtube.com	TRUE	/	TRUE	1796204908	__Secure-3PSIDTS	sidts-CjUBwQ9iIyzKnRhKFHwrOzVLhM8fMlFMSAehDL7CCOQAkGKXf0fDIOAaTRu9fYlyPLSRKzqlnhAA
.youtube.com	TRUE	/	FALSE	1796204908	SIDCC	AKEyXzVgljlis2cuqIldRA2pkQ6xsSQU9dtA8dcLSPN3qYb0s2DOZjJoJ04JNSLDiohmYK1CgQ
.youtube.com	TRUE	/	TRUE	1796204908	__Secure-1PSIDCC	AKEyXzW3Y_unLfCFvWpu_4VqK7fYpmUicOS_86yepNmYz3apAvYDPx_CpVP9wpv1TaBu7B9huA
.youtube.com	TRUE	/	TRUE	1796204908	__Secure-3PSIDCC	AKEyXzWEapxkBb5kSuN91soVoxY6FB-3kDpAx8vepxYX5vVT39uixswzqe1hXx_qPY4c581Qr0g
.youtube.com	TRUE	/	TRUE	0	YSC	hzsa1B54T9g
.youtube.com	TRUE	/	TRUE	1780220894	VISITOR_INFO1_LIVE	mI5miys20K8
.youtube.com	TRUE	/	TRUE	1780220894	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgIg%3D%3D
.youtube.com	TRUE	/	TRUE	1780143474	__Secure-ROLLOUT_TOKEN	CJnm7tjPwLq7WBCVr8qA2oCQAxjf97C_r5yRAw%3D%3D
"""

# ─── BOT / DATABASE CONFIG ──────────────────────────────────────────────────────
API_ID       = os.getenv("API_ID", "")
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
MONGO_DB     = os.getenv("MONGO_DB", "")
DB_NAME      = os.getenv("DB_NAME", "telegram_downloader")

# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
owner_id_str = os.getenv("OWNER_ID", "")
OWNER_ID     = list(map(int, owner_id_str.split())) if owner_id_str else []

STRING       = os.getenv("STRING", None)
LOG_GROUP    = int(os.getenv("LOG_GROUP", "-1001234456"))
FORCE_SUB    = int(os.getenv("FORCE_SUB", "-10012345567"))

# ─── SECURITY KEYS ──────────────────────────────────────────────────────────────
MASTER_KEY   = os.getenv("MASTER_KEY", "QWeCQl7F91DPGUdimsgic7_KwAKSx-NgQ8CAVBWaac8=")
IV_KEY       = os.getenv("IV_KEY", "HOl_k8Dypv6cG_6nIyYbxg==")

# ─── COOKIES HANDLING ───────────────────────────────────────────────────────────
YT_COOKIES   = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)

# ─── USAGE LIMITS ───────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "100000000000000000"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "50000000000000000000"))

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


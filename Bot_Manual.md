# 🤖 Save Restricted Content Bot v3 - Complete Manual

## 📖 Introduction
This bot is designed to save restricted content from Telegram channels/groups (even those with restricted saving) and download media from various platforms like YouTube, Instagram, etc. It supports bulk extraction, session-based login, and premium features.

---

## 🚀 Features
- **Restricted Content Saving**: Save text, media, and files from private/restricted Telegram channels.
- **Media Downloader**: Download videos/audio from YouTube, Instagram, and 30+ other sites.
- **Bulk Extraction**: Process multiple messages or entire channels in one go.
- **Session Login**: Log in with your Telegram account to access private channels you are a member of.
- **Custom Thumbnail**: Set custom thumbnails for your downloads.
- **Renaming**: Automatically rename files with custom prefixes/suffixes.
- **Premium System**: Manage paid users with expiration dates and limits.
- **Broadcast**: Send messages to all bot users.

---

## 🛠 Admin / Owner Commands
*Commands only usable by the bot owner (configured in `OWNER_ID`).*

| Command | Description | Usage |
|---------|-------------|-------|
| `/add` | Add a user to premium. | `/add <user_id>` |
| `/rem` | Remove a user from premium. | `/rem <user_id>` |
| `/get` | Get a list of all user IDs. | `/get` |
| `/lock` | Lock the channel from extraction. | `/lock` |
| `/stats` | View bot statistics (users, storage, etc.). | `/stats` |
| `/broadcast` | Broadcast a message to all users. | Reply to a message with `/broadcast` |

---

## 👤 User Commands

### 🔹 Basic
| Command | Description |
|---------|-------------|
| `/start` | Check if the bot is running and get the welcome message. |
| `/help` | Show the help menu with detailed instructions. |
| `/plan` | View premium plan details. |
| `/terms` | View terms and conditions. |
| `/myplan` | Check your current subscription status. |

### 🔹 Downloading & Extraction
| Command | Description | Usage |
|---------|-------------|-------|
| `/batch` | Bulk extract messages from a channel. | `/batch` (follow prompts) |
| `/dl` | Download video from a link (YouTube, Insta, etc.). | `/dl <link>` |
| `/adl` | Download audio from a link. | `/adl <link>` |
| `/cancel` | Cancel an ongoing batch process. | `/cancel` |

### 🔹 Account & Settings
| Command | Description |
|---------|-------------|
| `/login` | Log in with your Telegram account (via phone number). |
| `/logout` | Log out of the current session. |
| `/session` | Generate a Pyrogram v2 session string. |
| `/settings` | Configure custom settings (Thumbnail, Caption, etc.). |

---

## ⚙️ Settings Menu (`/settings`)
- **SETCHATID**: Set a custom channel/group to upload files to (e.g., `-100xxxx`).
- **SETRENAME**: Add a custom tag or username to file names.
- **CAPTION**: Set a custom caption for uploaded files.
- **REPLACEWORDS**: Replace specific words in filenames.
- **RESET**: Reset all settings to default.
- **THUMBNAIL**: Set a custom thumbnail for videos/audios.

---

## 🔧 Troubleshooting

### 🔴 YouTube Download Error: "Sign in to confirm you’re not a bot"
**Cause:** YouTube blocks data center IPs (like Koyeb) or requires authentication for certain videos.
**Fix:**
1. **Use Cookies:** You must provide valid `YT_COOKIES` in the environment variables.
2. **Refresh Cookies:** Cookies expire. Export fresh cookies from your browser (use an extension like "Get cookies.txt LOCALLY") and update the `YT_COOKIES` variable in Koyeb.
3. **Format:** Ensure cookies are in **Netscape format** (start with `# Netscape HTTP Cookie File`).

### 🔴 "Channel Invalid" or "User Not Participant"
**Cause:** The bot or your user account is not a member of the target channel.
**Fix:**
1. Ensure the **Bot** is an Admin in the `LOG_GROUP` and `FORCE_SUB` channel.
2. If using `/batch` for a private channel, you must be logged in via `/login`.

### 🔴 Bot Crashes / Restarting
**Cause:** Invalid configuration or memory limits.
**Fix:**
1. Check Koyeb logs.
2. If getting "FloodWait", wait for the specified time or regenerate the Bot Token.
3. Ensure `API_ID` and `API_HASH` are correct.

---

## 📝 Environment Variables (Koyeb)
- `API_ID`: Your Telegram API ID.
- `API_HASH`: Your Telegram API Hash.
- `BOT_TOKEN`: Your Bot Token from @BotFather.
- `OWNER_ID`: Your Telegram User ID.
- `MONGO_DB`: MongoDB Connection String.
- `LOG_GROUP`: ID of the log group (must start with `-100`).
- `FORCE_SUB`: ID of the force subscribe channel (must start with `-100`).
- `YT_COOKIES`: (Optional) Netscape format cookies for YouTube.
- `INSTA_COOKIES`: (Optional) Netscape format cookies for Instagram.

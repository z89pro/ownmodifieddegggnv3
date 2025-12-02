# plugins/plan.py

from pyrogram import Client, filters
from shared_client import app
from config import P0
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("plan"))
async def plan_command(client, message):
    text = (
        "💎 **PREMIUM PLANS** 💎\n\n"
        "Choose a plan that suits you best to unlock restricted content saving and 4GB upload support!\n\n"
        f"1️⃣ **{P0['d']['l']}**\n"
        f"   • Price: {P0['d']['s']} Stars\n"
        f"   • Validity: {P0['d']['du']} {P0['d']['u']}\n\n"
        f"2️⃣ **{P0['w']['l']}**\n"
        f"   • Price: {P0['w']['s']} Stars\n"
        f"   • Validity: {P0['w']['du']} {P0['w']['u']}\n\n"
        f"3️⃣ **{P0['m']['l']}**\n"
        f"   • Price: {P0['m']['s']} Stars\n"
        f"   • Validity: {P0['m']['du']} {P0['m']['u']}\n\n"
        "Use /pay command to purchase via Telegram Stars or contact Admin."
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Buy Now (/pay)", callback_data="pay_menu")],
        [InlineKeyboardButton("🆘 Contact Admin", url="https://t.me/kingofpatal")] 
    ])
    
    await message.reply_text(text, reply_markup=buttons)

@app.on_callback_query(filters.regex("^pay_menu"))
async def pay_menu_handler(client, query):
    await query.message.reply("Type /pay to proceed with payment!")
    await query.answer()

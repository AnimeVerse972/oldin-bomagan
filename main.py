import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiohttp import web
from keep_alive import keep_alive

TOKEN = os.getenv("BOT_TOKEN")  # Render'da .env faylga qo'shasiz
REQUIRED_CHANNEL = "@AniVerseClip"  # Majburiy obuna uchun kanal username

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except Exception:
        return False

@dp.message(CommandStart())
async def start(message: Message):
    if await is_subscribed(message.from_user.id):
        await message.answer("✅ Kanalga obuna bo‘lgansiz. Botdan foydalanishingiz mumkin.")
    else:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}")],
            [types.InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_subs")]
        ])
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "check_subs")
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if await is_subscribed(user_id):
        await callback_query.message.edit_text("✅ Rahmat! Endi botdan foydalanishingiz mumkin.")
    else:
        await callback_query.answer("⛔ Hali ham obuna bo‘lmagansiz.", show_alert=True)

# Webhook yoki polling ishga tushirish
async def on_startup(app: web.Application):
    print("Bot ishga tushdi")

if __name__ == "__main__":
    keep_alive()
    import asyncio
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

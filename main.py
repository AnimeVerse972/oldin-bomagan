import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode

TOKEN = os.getenv("BOT_TOKEN")  # Render .env fayliga qo‘shasiz
REQUIRED_CHANNEL = "@yourchannel"  # O'zingizning kanal username'ingizni yozing

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Obuna tekshirish funksiyasi
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.answer("✅ Siz kanalga obuna bo‘lgansiz. Xush kelibsiz!")
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("📢 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}"),
            types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs")
        )
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == "check_subs")
async def check_subs_handler(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.edit_text("✅ Rahmat! Siz endi botdan foydalanishingiz mumkin.")
    else:
        await call.answer("⛔ Hali ham obuna bo‘lmagansiz!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

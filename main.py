import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7731135599:AAGk1IGSXmHbDlTyT1YVsR-nzYhikNm9-jg"
REQUIRED_CHANNEL = "@AniVerseClip"  # Kanal username

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Obuna tekshirish funksiyasi
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# /start komandasi
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    subscribed = await is_subscribed(message.from_user.id)
    if subscribed:
        await message.reply("✅ Siz kanalga obuna bo‘lgansiz. Botdan foydalanishingiz mumkin.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📢 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}"))
        keyboard.add(types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_subs"))
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)

# Obunani qayta tekshirish
@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def check_subs(call: types.CallbackQuery):
    subscribed = await is_subscribed(call.from_user.id)
    if subscribed:
        await call.message.edit_text("✅ Rahmat! Endi botdan foydalanishingiz mumkin.")
    else:
        await call.answer("⛔ Hali ham obuna bo‘lmagansiz.", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

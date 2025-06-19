import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def is_user_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Xatolik: {e}")
        return False

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    is_subscribed = await is_user_subscribed(user_id)

    if is_subscribed:
        await message.answer("✅ Obuna bor. Botga xush kelibsiz!")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
        markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))
        await message.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_sub(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    is_subscribed = await is_user_subscribed(user_id)

    if is_subscribed:
        await callback_query.message.edit_text("✅ Obuna tekshirildi. Endi botdan foydalanishingiz mumkin.")
    else:
        await callback_query.answer("❗ Obuna yo‘q hali", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

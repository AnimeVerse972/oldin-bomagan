
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hlink
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
import os

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@AniVersrClip"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramBadRequest:
        return False

def subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
        [InlineKeyboardButton(text="🔄 Tekshirish", callback_data="check_subscribe")]
    ])
    return keyboard

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    is_subscribed = await check_subscription(message.from_user.id)
    if is_subscribed:
        await message.answer("👋 Salom! Botdan foydalanishingiz mumkin.")
    else:
        await message.answer(
            f"❗ Botdan foydalanish uchun quyidagi kanalga obuna bo‘ling:\n\n👉 {hlink('AniVersrClip kanaliga o‘tish', 'https://t.me/AniVersrClip')}",
            reply_markup=subscribe_keyboard()
        )

@dp.callback_query(F.data == "check_subscribe")
async def callback_check_subscription(callback_query):
    is_subscribed = await check_subscription(callback_query.from_user.id)
    if is_subscribed:
        await callback_query.message.edit_text("✅ Obuna tasdiqlandi! Botdan foydalanishingiz mumkin.")
    else:
        await callback_query.answer("⛔ Siz hali obuna bo‘lmagansiz.", show_alert=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from keep_alive import keep_alive

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Obuna uchun kanal
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keep_alive()

# ✅ Kod -> Kanal va message_id ma’lumotlari
anime_posts = {
    "1": {"channel": "@AniVerseClip", "message_id": 10},
    "2": {"channel": "@AniVerseClip", "message_id": 23},
    "3": {"channel": "@AniVerseClip", "message_id": 35},
    "4": {"channel": "@AniVerseClip", "message_id": 49},
    "5": {"channel": "@AniVerseClip", "message_id": 76},
    "6": {"channel": "@AniVerseClip", "message_id": 104},
    "7": {"channel": "@AniVerseClip", "message_id": 851},
    "8": {"channel": "@AniVerseClip", "message_id": 127},
    "9": {"channel": "@AniVerseClip", "message_id": 131},
    "10": {"channel": "@AniVerseClip", "message_id": 135},
    "11": {"channel": "@AniVerseClip", "message_id": 148},
    "12": {"channel": "@AniVerseClip", "message_id": 200},
    "13": {"channel": "@AniVerseClip", "message_id": 216},
    "14": {"channel": "@AniVerseClip", "message_id": 222},
    "15": {"channel": "@AniVerseClip", "message_id": 235},
    "16": {"channel": "@AniVerseClip", "message_id": 260},
    "17": {"channel": "@AniVerseClip", "message_id": 360},
    "18": {"channel": "@AniVerseClip", "message_id": 379},
    "19": {"channel": "@AniVerseClip", "message_id": 392},
    "20": {"channel": "@AniVerseClip", "message_id": 405},
    "21": {"channel": "@AniVerseClip", "message_id": 430},
    "22": {"channel": "@AniVerseClip", "message_id": 309},
    "23": {"channel": "@AniVerseClip", "message_id": 343},
    "24": {"channel": "@AniVerseClip", "message_id": 501},
    "25": {"channel": "@AniVerseClip", "message_id": 514},
    "26": {"channel": "@AniVerseClip", "message_id": 462},
    "27": {"channel": "@AniVerseClip", "message_id": 527},
    "28": {"channel": "@AniVerseClip", "message_id": 542},
    "29": {"channel": "@AniVerseClip", "message_id": 555},
    "30": {"channel": "@AniVerseClip", "message_id": 569},
    "31": {"channel": "@AniVerseClip", "message_id": 586},
    "32": {"channel": "@AniVerseClip", "message_id": 624},
    "33": {"channel": "@AniVerseClip", "message_id": 638},
    "34": {"channel": "@AniVerseClip", "message_id": 665},
    "35": {"channel": "@AniVerseClip", "message_id": 696},
    "36": {"channel": "@AniVerseClip", "message_id": 744},
    "37": {"channel": "@AniVerseClip", "message_id": 776},
    "38": {"channel": "@AniVerseClip", "message_id": 789},
    "39": {"channel": "@AniVerseClip", "message_id": 802},
    "40": {"channel": "@AniVerseClip", "message_id": 815},
    "41": {"channel": "@AniVerseClip", "message_id": 835},
    "42": {"channel": "@AniVerseClip", "message_id": 864},
    "43": {"channel": "@AniVerseClip", "message_id": 918},
    "44": {"channel": "@AniVerseClip", "message_id": 931},
    "45": {"channel": "@AniVerseClip", "message_id": 946}
}

# ✅ Obuna tekshirish funksiyasi
async def is_user_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if await is_user_subscribed(message.from_user.id):
        await message.answer("✅ Obuna bor. Kodni yuboring:")
    else:
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("📢 Obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"),
            types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
        )
        await message.answer("❗ Iltimos, kanalga obuna bo‘ling:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_subscription(callback_query: types.CallbackQuery):
    if await is_user_subscribed(callback_query.from_user.id):
        await callback_query.message.edit_text("✅ Obuna tekshirildi. Kod yuboring.")
    else:
        await callback_query.answer("❗ Hali ham obuna emassiz!", show_alert=True)

# 💬 Kod yuborilsa — kanal postini link orqali chiqarish va tugma bilan
@dp.message_handler(lambda msg: msg.text.strip().isdigit())
async def handle_code(message: types.Message):
    code = message.text.strip()

    if not await is_user_subscribed(message.from_user.id):
        await message.answer("❗ Koddan foydalanish uchun avval kanalga obuna bo‘ling.")
        return

    if code in anime_posts:
        try:
            post = anime_posts[code]
            channel_username = post['channel'].lstrip('@')
            message_id = post['message_id']
            post_url = f"https://t.me/{channel_username}/{message_id}"

            # 1️⃣ Postni kanaldan nusxalab yuborish
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=post['channel'],
                message_id=message_id
            )

            # 2️⃣ Tugmani alohida xabar sifatida yuborish (matn bilan)
            buttons = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("📥 Yuklab olish", url=post_url)
            )

            await bot.send_message(
                chat_id=message.chat.id,
                text="⬇️ Yuklab olish tugmasi:",
                reply_markup=buttons
            )

        except Exception as e:
            await message.answer("⚠️ Kod topildi, lekin postni yuborib bo‘lmadi.")
            print(f"[Xatolik] {e}")
    else:
        await message.answer("❌ Bunday kod topilmadi.")


# 🟢 Botni ishga tushuramiz
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

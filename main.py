import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("👋 Привет! Отправь номер телефона, и я пришлю ссылку для WhatsApp.")

@dp.message_handler()
async def phone_handler(message: types.Message):
    raw = message.text.strip()
    clean = re.sub(r"[^0-9+]", "", raw)

    if clean.startswith('+'):
        clean = clean[1:]
    elif len(clean) in (9, 10):
        clean = '7' + clean

    if clean.isdigit() and len(clean) >= 10:
        wa_url = f"https://wa.me/{clean}"
        await message.reply(f"🔗 Вот ваша ссылка для WhatsApp:\n{wa_url}")
    else:
        await message.reply("❌ Неверный номер. Попробуйте снова.")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

import asyncio
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from keep_alive import keep_alive

TOKEN = "7214940614:AAGGxZGvXmP9iCkyReML9QjhrKaBlY7Bp60"
bot = Bot(token=TOKEN)
dp = Dispatcher()
TOKEN = os.getenv("BOT_TOKEN")

TOKEN = os.getenv("TOKEN")

def download_video(url):
    output_path = "downloads/%(title)s.%(ext)s"
    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("👋 Hello! Send a video link (YouTube, TikTok, etc.) to download.")

@dp.message()
async def handle_message(message: Message):
    url = message.text.strip()
    if any(site in url for site in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com", "pinterest.com"]):
        await message.reply("⏳ Downloading your video...")
        try:
            video_path = download_video(url)
            await message.answer_document(types.FSInputFile(video_path))
            os.remove(video_path)
        except Exception as e:
            await message.reply(f"❌ Error: {e}")
    else:
        await message.reply("❌ Invalid link. Please send a valid video URL.")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

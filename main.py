import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start
from db.database import create_pool, create_tables

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)

    await create_pool()
    await create_tables()

    print("LimonFood bot ishga tushdi! 🍋")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
